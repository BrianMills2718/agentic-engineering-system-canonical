# Plan 002 P0 closure runbook

Status: executable handoff; **P0 is not yet closed**
Plan authority: `docs/plans/002_offline_policy_decision_replay.md`
Case inventory: `evals/plan-002/case_manifest.json`
Execution tracker: Issue #20

This runbook exists so the next machine-capable session performs the remaining discriminating checks rather than repeating GitHub research. It does not weaken Plan 002's stop rule and does not authorize V1 implementation by itself.

## Exit condition

P0 closes only when all of the following are retained:

- [ ] the current conversation exposes Remote MCP `devices_list`, `devices_ping`, and `process_start`;
- [ ] the intended device is present, `execution_ready`, and responds to `devices_ping`;
- [ ] at least **5 authentic** completion/verification decision events have exact source/session/repository/revision identity;
- [ ] the selected cases' raw transcript/receipt bytes are still available under their existing owner/custody and match retained hashes where hashes already exist;
- [ ] each selected case has enough event-time state to reconstruct the incumbent decision without using later outcome/adjudication;
- [ ] TypeSafe authentication works;
- [ ] `GET https://api.typesafe.ai/v1/models` succeeds and the response is retained by digest;
- [ ] one exact model identity used for the smoke request is retained from the **response**;
- [ ] one protocol-only `POST /v1/systemone` succeeds;
- [ ] no private raw transcript, API key, or unrelated secret is copied into Git.

If any required item fails, record the exact blocker and stop. Do not replace the provider, create a transcript platform, or widen the policy family to manufacture progress.

## 1. Execution-readiness preflight

Follow `CLAUDE.md#execution-readiness-preflight` exactly.

1. Confirm `devices_list`, `devices_ping`, and `process_start` exist in the current conversation.
2. If `devices_list` is absent: classify **SESSION_TOOL_NOT_EXPOSED** and stop machine work.
3. Call `devices_list`; normally select `WINDOWS-STQ88HK` only if it reports `execution_ready`.
4. Call `devices_ping`.
5. Only after a successful ping inspect local files or launch the guarded WSL path.

Do not interpret a missing chat tool as a machine, WSL, repository, or provider failure.

## 2. Resolve one uncounted authentic lead into case five

Prefer the 2026-09-22 live scope-mismatch family because it contains four real Claude Code turns that reached the judge and returned `claim_support_rejected:1_of_1`.

Source observation:

`Inside-Success/agentic-engineering-system@418f1782b55f68cc332feee6848eb6116ba9fd10`

`evidence/propagation/2026-09-22-gate-fix-and-scope-mismatch/README.md`

The source revision recorded by that observation is:

`8e91acf5b2c6acf02f3f9a3c2a9be13c4a6e8a7c`

### 2.1 Find the authentic transcript

Inside the guarded WSL environment, search existing Claude archives; do not alter them:

```bash
set -euo pipefail

rg -l --hidden --glob '*.jsonl' 'echo hi4|printed hi4|bash echo hi4' \
  ~/.claude/projects 2>/dev/null
```

If `hi4` is not retained, repeat for `hi1`, `hi2`, and `hi3`.

For each plausible transcript:

```bash
TRANSCRIPT=/exact/path/from-search.jsonl
SESSION_ID="$(basename "$TRANSCRIPT" .jsonl)"
TRANSCRIPT_SHA256="$(sha256sum "$TRANSCRIPT" | awk '{print $1}')"

printf 'session_id=%s\ntranscript_sha256=%s\n' "$SESSION_ID" "$TRANSCRIPT_SHA256"
```

Do **not** paste the transcript body into Git or chat merely to prove it exists.

### 2.2 Locate the original decision receipt or hook record

First derive the session bucket identity:

```bash
SESSION_SHA256="$(printf '%s' "$SESSION_ID" | sha256sum | awk '{print $1}')"
printf 'session_id_sha256=%s\n' "$SESSION_SHA256"
```

Search high-signal existing stores before any broad filesystem scan:

```bash
rg -l --hidden \
  'claim_support_rejected:1_of_1|no_report' \
  ~/.claude/coordination ~/.claude/projects ~/code ~/projects 2>/dev/null || true

find ~/.claude ~/code ~/projects \
  -path "*/receipts/${SESSION_SHA256}/*/completed.json" \
  -type f -print 2>/dev/null || true
```

If a completed receipt is found:

```bash
RECEIPT=/exact/path/completed.json
RECEIPT_SHA256="$(sha256sum "$RECEIPT" | awk '{print $1}')"

jq '{
  decision,
  reason_code,
  receipt_id,
  input_sha256,
  report_sha256,
  session_id_sha256,
  observed_at,
  origin_kind,
  event_name,
  phase
}' "$RECEIPT"

printf 'receipt_sha256=%s\n' "$RECEIPT_SHA256"
```

If only a raw hook-invocation record survives, retain its path/digest and the exact decision-bearing payload identity. Do not manufacture a receipt identity.

### 2.3 Verify event-time reconstruction

For the fifth case, retain only the minimum facts needed to demonstrate:

- exact session identity;
- exact transcript digest;
- source repository + source revision;
- the assistant claim/report actually presented at the protected boundary;
- current-turn tool evidence visible **at that boundary**;
- original decision/reason when recoverable;
- exact hook/control revision when recoverable;
- explicit statement of which later fields/outcomes are withheld from evaluator input.

A finished transcript may contain information written **after** the synchronous Stop decision. Do not treat later-written bytes as event-time state merely because they are in the same final JSONL. Use retained hook payload/receipt timing or the source observation to separate them.

### 2.4 Promote the lead only when exact

Update `evals/plan-002/case_manifest.json` only after the raw check.

Promotion rule:

```text
authentic observation
+ exact session/transcript identity
+ repository/revision identity
+ event-time reconstruction adequate
= counted P0 case
```

Receipt identity is strongly preferred. If the original receipt has been legitimately lost but the authentic event-time input and deterministic decision can be reproduced from the exact historical implementation, record that limitation explicitly rather than inventing bytes.

## 3. Verify custody for the existing four cases

For each currently counted case, use the exact session IDs and SHA-256 values in `case_manifest.json`.

Minimum check:

```bash
TRANSCRIPT=/resolved/path/from-session-id.jsonl
test "$(sha256sum "$TRANSCRIPT" | awk '{print $1}')" = "<manifest transcript_sha256>"
```

For receipts whose original bytes still exist:

```bash
RECEIPT=/resolved/path/completed.json
test "$(sha256sum "$RECEIPT" | awk '{print $1}')" = "<manifest receipt_sha256>"
```

If an original temporary receipt no longer exists but a sanitized repository projection preserved its exact source digest and decision payload, record the custody limitation honestly. P0 needs replayable authentic decision evidence; it does not require resurrecting deleted `/tmp` paths.

## 4. TypeSafe/Jev authenticated provider preflight

Current official TypeSafe API documentation says:

- authenticate with `Authorization: Bearer <API_KEY>`;
- discover account-available names with `GET /v1/models`;
- evaluate state with `POST /v1/systemone`;
- requests contain `state`, `model`, and named typed `questions`.

Never commit or echo the key.

### 4.1 Discover models

```bash
set -euo pipefail
: "${TYPESAFE_API_KEY:?TYPESAFE_API_KEY must be set outside Git}"

OUT="$(mktemp -d)"
chmod 700 "$OUT"

curl --fail-with-body --silent --show-error \
  https://api.typesafe.ai/v1/models \
  -H "Authorization: Bearer ${TYPESAFE_API_KEY}" \
  -H 'Accept: application/json' \
  > "$OUT/models.json"

jq -e '.models | type == "array" and length > 0' "$OUT/models.json" >/dev/null
jq '.models | map({name, description, release_date})' "$OUT/models.json"
sha256sum "$OUT/models.json"
```

Choose one returned model name for the protocol smoke. The first smoke is not an accuracy test.

### 4.2 Protocol-only smoke request

Use a trivial state unrelated to any real policy case:

```bash
MODEL="$(jq -r '.models[0].name' "$OUT/models.json")"

jq -n --arg model "$MODEL" '{
  state: {
    probe: "plan002-protocol-smoke",
    purpose: "verify TypeSafe request/response plumbing only"
  },
  model: $model,
  questions: {
    probe_present: {
      type: "noul",
      instructions: "Does the state contain the exact probe value plan002-protocol-smoke?",
      criteria: {
        true: "The exact probe value is present.",
        false: "The exact probe value is absent."
      }
    }
  }
}' > "$OUT/smoke-request.json"

curl --fail-with-body --silent --show-error \
  https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer ${TYPESAFE_API_KEY}" \
  -H 'Content-Type: application/json' \
  --data-binary @"$OUT/smoke-request.json" \
  > "$OUT/smoke-response.json"

jq -e '.model and .answers.probe_present and .usage' "$OUT/smoke-response.json" >/dev/null
jq '{model, answers, usage}' "$OUT/smoke-response.json"
sha256sum "$OUT/smoke-request.json" "$OUT/smoke-response.json"
```

The exact model identity returned by `.model` is the identity to retain for this smoke. If the response omits an exact version and returns only an alias, record that limitation; do not infer a hidden immutable version.

This call proves only authentication, schema/protocol compatibility, and one successful provider response. It is **not** evidence that Jev is accurate enough for Plan 002.

## 5. Durable P0 closeout record

When the checks above complete, update:

- `evals/plan-002/case_manifest.json`;
- `evals/plan-002/README.md`;
- `docs/plans/002_offline_policy_decision_replay.md`;
- Issue #20;
- a new revision-bound record under `evidence/plan-002/<aes-revision>/p0-preflight.json`.

The P0 evidence record should contain metadata/digests only:

```json
{
  "p0_status": "passed",
  "authentic_case_count": 5,
  "case_manifest_sha256": "...",
  "raw_custody_checked": true,
  "typesafe_models_response_sha256": "...",
  "requested_model": "...",
  "response_model": "...",
  "smoke_request_sha256": "...",
  "smoke_response_sha256": "...",
  "provider_protocol_result": "passed",
  "secrets_retained_in_git": false
}
```

Do not retain the API key, raw private transcripts, or unrelated provider/account metadata.

## 6. What P0 success authorizes

P0 success authorizes **V1 implementation for one authentic offline replay**.

It does not authorize:

- live Claude Code/Codex hooks;
- warnings or enforcement;
- a broad archive/capture platform;
- a universal policy registry;
- additional policy families;
- automated policy changes;
- a claim that Jev improves AES.

Those decisions remain downstream of V1/V2 evidence.
