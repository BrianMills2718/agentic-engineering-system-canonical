# AES-specific architecture

This directory contains AES-specific normative and delivery architecture for the canonical convergence project. Project-agnostic methodology remains owned by `BrianMills2718/wiki_methodology` at the revision declared in `.agentic/repo.yaml`; generic planning-method improvements should be proposed to Company Planning rather than silently duplicated here.

**AES v0.2 (accepted, [Decision 0010](../decisions/0010-greenfield-v0.2-accepted.md)):** start at [`greenfield-v0.2/`](greenfield-v0.2/README.md). It governs `src/agentic_engineering_system/` and `tests/greenfield/` through `.aes/target.yaml`. The files listed below are the v0.1 bootstrap architecture, retained under Decision 0010's v0.1 disposition.

Read in this order (v0.1):

1. [`SYSTEM_BOUNDARY.md`](SYSTEM_BOUNDARY.md) — canonical AES clauses and subsystem boundaries.
2. [`HUMAN_OBSERVABLE_DELIVERY.md`](HUMAN_OBSERVABLE_DELIVERY.md) — AES delivery constraints for human-observable slices, experience-backward design, feasibility probes, utility/conformance separation, attention checkpoints, and execution economics.
3. [`INITIAL_GAP_LEDGER.md`](INITIAL_GAP_LEDGER.md) — bootstrap target/current variance and dispositions. Treat it as a planning input until fresh implementation characterization recomputes current/gap state.
4. [`normative-component-alignment.bootstrap.yaml`](normative-component-alignment.bootstrap.yaml) — resolved bootstrap design record and next real dogfood gate.
5. [`normative-record-model.bootstrap.yaml`](normative-record-model.bootstrap.yaml) — accepted bootstrap target model for compact system/component normative records; existing accepted Markdown remains authority until an explicit cutover.
6. [`aes-company-planning-profile.bootstrap.yaml`](aes-company-planning-profile.bootstrap.yaml) — AES-local profile over Company Planning, including reproducible bootstrap validation commands.
7. [`schemas/architecture-realization.bootstrap.schema.json`](schemas/architecture-realization.bootstrap.schema.json) — minimal machine-readable architecture-realization contract.

## Authority and generated material

- `docs/decisions/` owns accepted AES architecture choices and their rationale.
- The bootstrap YAML records above define AES-local profile/model/schema state but do not silently migrate existing accepted Markdown authority.
- `generated/bootstrap-normative/` is generated dogfood/probe material, not editable normative authority.
- `architecture-realization.bootstrap.yaml` is superseded exploratory research history; do not use it as the current design packet.
- Research and evidence support decisions but do not become normative merely by being referenced.

These documents may specialize how canonical AES applies upstream methodology, but they should not silently fork project-agnostic rules. Reusable friction or improvements belong upstream once dogfood evidence supports them.
