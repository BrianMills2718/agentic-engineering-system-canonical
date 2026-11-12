"""`pcw`: Lockstep's old package name, kept as an alias of `lockstep`.

lifelike's Makefile and Team-Brains' brain runner call `python -m pcw.<module>` and cog blocks say
`import pcw.cogtext`; this package resolves every `pcw.<module>` to the module of the same name in
`lockstep`, so they keep working until they move (one-planning-tool design, slices 1 and 6).
"""

import lockstep

__path__ = list(lockstep.__path__)
