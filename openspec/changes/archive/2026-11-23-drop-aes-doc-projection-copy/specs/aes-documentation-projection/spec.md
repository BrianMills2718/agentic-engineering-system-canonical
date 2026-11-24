## REMOVED Requirements

### Requirement: AES projects its source-owned component assessment

**Reason**: Repeats `lockstep-doc-facts` "Declared source facts have one authority" for AES's declared projections.
Brian, 2026-11-23: "i approve", to Q51.

**Migration**: AES's `projections:` in `lockstep.yaml` follow `lockstep-doc-facts`; nothing changes in the code.

### Requirement: AES checks declared fact freshness without broad regeneration

**Reason**: Repeats `lockstep-doc-facts` "Installed edit and merge paths maintain facts"; `make check-doc-facts`
already runs that check in AES. Brian, 2026-11-23: "i approve", to Q51.

**Migration**: None; `make check` keeps running `check-doc-facts`.
