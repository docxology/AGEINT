# Release and Change Control: reuse approval, rollback, and change evidence

AGEINT artifacts are not deployed systems, but reuse still needs a release gate:
an instructor should know what changed, what was tested, what can roll back, and
what monitoring signal would reopen review.

## Gates: source freshness, safety review, validation, and rollback proof

| Gate | Evidence |
|---|---|
| Scope freeze | accountable use case, excluded actions, tool profile, and data boundary |
| Security and rights review | privacy, accessibility, security, bias, and human-review checks |
| Version and rollback | model, prompt, dataset, or rubric version; changelog; test fixture; rollback path |
| Post-release monitoring | monitoring signal, incident threshold, refresh trigger, and owner |

The gate is grounded in NIST SP 800-218A, CISA joint guidance on deploying AI
systems securely, NIST AI 600-1, and NIST Dioptra evaluation evidence. Any
artifact that drifts toward live target interaction, external action, or unsafe
cyber-physical behavior is held and rewritten as tabletop or audit work.
