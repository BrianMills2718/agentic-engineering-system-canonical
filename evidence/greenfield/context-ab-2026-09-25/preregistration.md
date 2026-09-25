# Context A/B rerun — pre-registration (2026-09-25, AES canonical at 2509ea4)

Change under test: `aes status`/`aes reconcile` report ER-SC-GF-005-02 and
ER-SC-GF-009-01 as "no route" although each has an `external_boundaries` entry
in `.aes/target.yaml` and `aes target validate` accepts them. Fix: an evidence
requirement with an external boundary is routed.

Arm A: change request + `aes context RU-AES-RECONCILE` packet + repository.
Arm B: change request + repository; told to read README first. Separate agent
sessions, no access to this conversation or the proposals directory (B is not
told the proposals directory exists; A's packet does not mention it either).
Note: the packet omits SC-GF-004 (the "no route" criterion) because
RU-AES-RECONCILE's target_refs do not include it — recorded as a packet
limitation before the run.

Obligations (scored missed/met from the arm's commit + report):
1. `has_route` is true for an ER named in `external_boundaries`.
2. ERs with neither subject nor boundary still report "no route".
3. Test added in `tests/greenfield/test_reconcile.py` covering both 1 and 2.
4. Full `tests/greenfield` passes.
5. No new file under governed roots unless added to `.aes/target.yaml` first.
6. Commit passes the installed pre-commit hook (no --no-verify).
7. Evidence recorded after the commit: `aes evidence record VS-GF-RECONCILE`
   (AGENTS.md rule), observation file committed.
8. `aes status` on the clone shows `0 unsupported evidence requirement(s) with no route`.

Measures: files read (from the arm's own list), obligations missed, topology
violations (hook rejections), rework (commits after the first), wall time.
