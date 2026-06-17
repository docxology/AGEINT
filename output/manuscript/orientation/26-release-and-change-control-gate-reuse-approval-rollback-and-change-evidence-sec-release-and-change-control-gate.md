## Release and change-control gate: reuse approval, rollback, and change evidence {#sec:release-and-change-control-gate}

| Gate | Release evidence | Block condition |
|---|---|---|
| Scope freeze | accountable use case, excluded actions, tool profile, and data boundary | scope expands to external action, live data, or an unreviewed capability |
| Security and rights review | privacy, accessibility, security, bias, and human-review checks | rights impact, vulnerability, or accessibility issue has no owner |
| Version and rollback | model or prompt version, changelog, test fixture, and rollback path | change cannot be reproduced, compared, or reverted |
| Post-release monitoring | monitoring signal, incident threshold, refresh trigger, and owner | deployment or reuse occurs without logging and retest commitments |
