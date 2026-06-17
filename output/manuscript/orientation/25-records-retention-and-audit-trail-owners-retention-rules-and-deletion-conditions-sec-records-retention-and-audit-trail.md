## Records retention and audit trail: owners, retention rules, and deletion conditions {#sec:records-retention-and-audit-trail}

| Record | Retained fields | Audit question |
|---|---|---|
| Source and prompt register | source identity, prompt version, tool allowlist, reviewer, timestamp, and caveat | Can a later reviewer reconstruct the evidentiary path without private or live data? |
| Decision and exception log | risk owner, accepted exception, compensating control, expiry date, and approval | Is every deviation time-bound, justified, and reviewable? |
| Artifact retention note | output type, sensitivity, access boundary, deletion rule, and refresh trigger | Does the retention choice match the educational purpose and rights impact? |
| Incident and remediation record | incident signal, containment action, root cause, owner, retest result, and closure date | Can the same failure be detected and prevented in the next reuse cycle? |
