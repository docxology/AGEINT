## Add or extend a citation: preserve identity and record metadata

**Navigation.** Parent section: [@sec:bibliography_atlas].

1. Preserve `ageint001` through `ageint231`; do not renumber locked source identities.
2. Append new source-guide references after the locked range. Current generated guide keys extend through `ageint312`.
3. For curated anchors, record `source_lane`, `source_tier`, `checked_as_of`, `verification_method`, `claim_scope`, `refresh_cadence`, `refresh_trigger`, `stakeholder_role`, `assurance_use`, and `rights_dimension`.
4. Use Pandoc citation syntax such as `[@ageint137]` or `[@official_nist_ai_rmf]`.
5. Use label-backed cross-references to the curriculum orientation section and curriculum-map figure rather than hard-coded section or figure numbers.
6. Rebuild from the AGEINT root:

```bash
uv run python scripts/build_curriculum.py
```
