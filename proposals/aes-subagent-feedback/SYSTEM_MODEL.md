# Subagent feedback system model

This extends the [existing loop](../aes-learning-loop/PLAN.md) without another store.

| Element | Evidence and behavior |
| --- | --- |
| Assignment | Parent session, native call ID, role, recorded packet digest and context mode; raw packet stays private. |
| Native outcome | Child reference and observed completion, failure or cancellation; completion is unverified by default. Occurrence time comes from the native result, even when checked later; missing times stay unknown. |
| Child execution | Exact trace reference and observed runtime model/effort/context; missing values stay unknown. |
| Parent check | Parent executes checks on exact returned bytes; receipt binds call, child, result digest, commands, output and exit. Checker failure is a separate event at check time, not a child-quality judgment. |
| Feedback report | Existing feedback-report.v1 records plus attributable subagent metadata in the report envelope. |
| Storage and view | Existing reports daily JSONL, state.sqlite deduplication and private agent-feedback-log issue. |
| Improvement | Existing weekly reader generalizes failures; agents change role methods, handoffs, skills or shared controls where evidence points. |
| Prevention | Existing explicit enforcement receipts and daily reported-recurrence watcher apply unchanged. |

The canary must show one assignment identity through native outcome, parent check, stored report, private issue and weekly reader membership. Capture cannot establish a cause or prove a model is unsuitable; those require trace-supported analysis.
