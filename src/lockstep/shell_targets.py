"""Which paths a shell command writes: the parser the edit hook judges shell commands by (behavior 5.1).

Ported from code2check's guard (code2-template `src/code2check/guard.py` at revision 6ce00a9, pull
requests 25 and 26): `segments`, `command_writes` and the code-writes rule are its code, with two
changes Lockstep needs. Redirect and tee targets are read from shell words (so `echo 'a > b.py'` names no
file), and `written_paths` follows `cd`. This reads command text (code), never prose.

A simple command writes a word when the word is its redirect or tee target, when the command is one that
writes what it names (`mv`, `touch`, `truncate`, `sed -i`, `perl -i`, `dd of=`; a copy (`cp`, `install`,
`rsync`) writes only its destination), or when code in it (a `python -c`, a heredoc script) calls
something that writes, in which case every path it names counts. A command that only reads a file
(`cp planned /tmp/x`, `python -c "open(p).read()"`) writes nothing.

Implements: lockstep-guard/shell-commands-are-judged-by-the-paths-they-write
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import shlex

# A heredoc operator (`<<EOF`, `<<-'EOF'`, not a `<<<` here-string); its body belongs to that command.
_HEREDOC = re.compile(r"(?<!<)<<-?\s*(['\"]?)([A-Za-z_][\w-]*)\1")
_WORD = re.compile(r"[^\s'\"`;&|<>(),=]+")
_REDIRECT = re.compile(r"(?:^|\s)\d?>>?(?!&)\s*['\"]?([^\s;&|'\"]+)")
_TEE = re.compile(r"\btee\s+(?:-a\s+)?['\"]?([^\s;&|'\"]+)")
_REDIRECT_WORDS = {">", ">>", ">|", "&>", "&>>"}
_CD = re.compile(r"^\s*\(?\s*(?:cd|pushd)\s+(?:--\s+)?(['\"]?)([^\s'\";&|()]+)\1\s*\)?\s*$")
# Code in a command writes the paths it names only when it calls something that writes; `open(p)` or
# `open(p, "r")` alone only reads.
_CODE_WRITES = re.compile(
    r"\.write\(|\.writelines\(|write_text|write_bytes|\.touch\(|\.unlink\(|\.rename\(|"
    r"\bos\.(?:remove|unlink|replace|rename|truncate)\b|\bshutil\.|\b(?:json|pickle|yaml|toml|tomli_w)\.dump\(|"
    r"\bfile\s*=|\.open\(\s*['\"][wax]|\bopen\(\s*[^,()]*,(?!\s*(?:['\"]r[bt]?['\"]|mode\s*=\s*['\"]r[bt]?['\"])\s*[,)])"
)
# Words that run the next word as the command (`sudo cp ...`), and redirects, dropped before reading words.
_WRAPPERS = {"sudo", "env", "command", "builtin", "exec", "nohup", "time", "nice", "doas"}
_REDIRECTION = re.compile(r"\d?(?:>>?|<<?<?)&?-?\s*(?:'[^']*'|\"[^\"]*\"|[^\s;&|]+)")
# Commands that write every file they name, and copies that write only their destination.
_WRITE_ALL = {"mv", "touch", "truncate"}
_COPIES = {"cp", "install", "rsync"}


def segments(command: str) -> list[str]:
    """Split a shell command into simple commands, each heredoc body joined to the command that opens it.

    `;`, `|` and newlines inside quotes belong to the word (a `python -c` script); a command that opens a
    heredoc carries its body after a newline.
    """
    out: list[str] = []
    opened: list[tuple[int, str]] = []  # (segment index, delimiter) of heredocs opened on this line
    cur, quote, i, n = "", "", 0, len(command)

    def close() -> None:
        nonlocal cur
        opened.extend((len(out), m.group(2)) for m in _HEREDOC.finditer(cur))
        out.append(cur)
        cur = ""

    while i < n:
        c = command[i]
        if quote:
            cur += c
            if c == "\\" and quote == '"' and i + 1 < n:
                cur += command[i + 1]
                i += 1
            elif c == quote:
                quote = ""
            i += 1
        elif c in "'\"":
            quote, cur, i = c, cur + c, i + 1
        elif c == "\\" and i + 1 < n:
            cur, i = cur + command[i:i + 2], i + 2
        elif command.startswith(("&&", "||"), i):
            close()
            i += 2
        elif c in ";|":
            close()
            i += 1
        elif c == "\n":
            close()
            i += 1
            for index, delimiter in opened:
                body = []
                while i < n:
                    end = command.find("\n", i)
                    end = n if end < 0 else end
                    line, i = command[i:end], end + 1
                    if line.strip() == delimiter:
                        break
                    body.append(line)
                out[index] += "\n" + "\n".join(body)
            opened.clear()
        else:
            cur, i = cur + c, i + 1
    close()
    return out


def _head(segment: str) -> str:
    """The segment without its heredoc body: the first line when the segment opens a heredoc, else all of it."""
    first = segment.split("\n", 1)[0]
    return first if _HEREDOC.search(first) else segment


def command_writes(head: str) -> list[str]:
    """The words a simple command writes by what the command is, not by redirects or code.

    The command is the first word after variable assignments and wrappers such as `sudo`. `mv`, `git mv`,
    `touch` and `truncate` write every path they name; `cp`, `install` and `rsync` write only their
    destination (the last path, or the `-t` folder; every path for `install -d`); `dd` writes its `of=`
    file; `sed` and `perl` write their files only with `-i`.
    """
    head = _REDIRECTION.sub(" ", head).rstrip().rstrip("\\")  # a `\;` ends find's -exec; `;` split it off
    try:
        words = shlex.split(head)
    except ValueError:
        words = _WORD.findall(head)
    return _named_writes(words)


def _named_writes(words: list[str]) -> list[str]:
    """`command_writes` for a simple command already split into words."""
    while words and (re.match(r"[A-Za-z_]\w*=", words[0]) or words[0] in _WRAPPERS or words[0] == "timeout"):
        words = words[2:] if words[0] == "timeout" and len(words) > 1 and not words[1].startswith("-") else words[1:]
    if len(words) > 1 and words[0] == "git" and words[1] == "mv":
        words = words[1:]
    if not words:
        return []
    name, args = Path(words[0]).name, words[1:]
    if name in ("bash", "sh", "zsh", "dash"):
        k = next((k for k, a in enumerate(args) if re.fullmatch(r"-[a-z]*c[a-z]*", a)), None)
        script = " ".join(args[k + 1:]) if k is not None else ""
        return [w for part in segments(script) for w in command_writes(part.split("\n", 1)[0])]
    if name == "xargs":
        while args and args[0].startswith("-"):
            args = args[2:] if args[0] in ("-I", "-n", "-P", "-L", "-d", "-E", "-s", "-a") else args[1:]
        return _named_writes(args)
    if name == "find":
        hits = []
        for k, a in enumerate(args):
            if a in ("-exec", "-execdir", "-ok", "-okdir"):
                end = next((j for j in range(k + 1, len(args)) if args[j] in (";", "+")), len(args))
                hits += _named_writes(args[k + 1:end])
        return hits
    paths = [a for a in args if not a.startswith("-")]
    if name in _WRITE_ALL:
        return paths
    if name == "dd":
        return [a[3:] for a in args if a.startswith("of=")]
    if name == "sed":
        return paths if any(a.startswith(("-i", "--in-place")) for a in args) else []
    if name == "perl":
        return paths if any(re.fullmatch(r"-[a-zA-Z]*i\S*", a) for a in args) else []
    if name in _COPIES:
        if name == "install" and "-d" in args:
            return paths
        for k, a in enumerate(args):
            if a in ("-t", "--target-directory") and k + 1 < len(args):
                return [args[k + 1]]
            if a.startswith("--target-directory="):
                return [a.split("=", 1)[1]]
        return paths[-1:]
    return []


def _redirect_targets(head: str) -> list[str]:
    """Redirect and tee targets in a simple command's words; quoted text such as `echo 'a > b'` names none."""
    try:
        lex = shlex.shlex(head, posix=True, punctuation_chars=True)
        lex.whitespace_split = True
        words = list(lex)
    except ValueError:  # unbalanced quotes: fall back to the command-text patterns
        return _REDIRECT.findall(head) + _TEE.findall(head)
    sure = [words[k + 1] for k, w in enumerate(words[:-1]) if w in _REDIRECT_WORDS]
    if "tee" in words:
        for w in words[words.index("tee") + 1:]:
            if w and w[0] in "|;&<>()":
                break
            if not w.startswith("-"):
                sure.append(w)
    return sure


def _code_paths(segment: str) -> list[str]:
    """The path-like words in code that writes: a word with a `/`, or a `name.ext` word the code quotes.

    Code is not shell, so `python`, `open`, `.write` and `os.path.join` are not paths; a bare name counts only as a string literal.
    """
    return [w for w in _WORD.findall(segment)
            if "/" in w or (re.fullmatch(r"[\w-]+\.[A-Za-z0-9]+", w) and re.search(r"['\"]" + re.escape(w) + r"['\"]", segment))]


def shell_write_words(command: str) -> list[str]:
    """The words, as written, that `command` writes: redirect and tee targets, what a command writes by what
    it is, and every path named by code that calls something that writes. Each once, in order."""
    return [w for _, words in _by_segment(command) for w in words]


def _by_segment(command: str) -> list[tuple[str, list[str]]]:
    out = []
    for segment in segments(command):
        head = _head(segment)
        targets = _redirect_targets(head) + command_writes(segment.split("\n", 1)[0])
        if _CODE_WRITES.search(segment):
            targets += _code_paths(segment)
        out.append((segment, [w for w in dict.fromkeys(targets) if w and not w.startswith("-")]))
    return out


def written_paths(command: str, cwd: Path) -> list[Path]:
    """The paths `command` writes, absolute, resolved against `cwd` and following `cd` and `pushd` between commands."""
    here, hits = cwd, []
    for segment, words in _by_segment(command):
        cd = _CD.match(segment)
        if cd:
            step = Path(os.path.expanduser(cd.group(2)))
            here = step if step.is_absolute() else here / step
            continue
        for word in words:
            path = Path(os.path.expanduser(word))
            path = path if path.is_absolute() else here / path
            if path not in hits:
                hits.append(path)
    return hits
