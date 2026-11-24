# AGEINT Claim Calibration

| Measure | Value |
|---|---:|
| OK | true |
| Generated at | 2026-11-06T23:12:04+00:00 |
| Candidate rows | 8081 |
| Hard-fail rows | 0 |
| Review-warning rows | 4729 |
| Boundary-allowed rows | 478 |

## Claim Class Distribution

| Claim class | Rows |
|---|---:|
| artifact_readiness | 282 |
| empirical_or_evaluation | 1007 |
| figure_or_visualization | 495 |
| formalism_or_statistical_expression | 2 |
| governance_or_rights | 2831 |
| safety_or_assurance | 3464 |

## Source Support Distribution

| Source support distribution | Mentions |
|---|---:|
| curated_context | 12 |
| law_policy_primary | 14 |
| mirror_or_copy_context | 30 |
| official_primary | 872 |
| practitioner_or_vendor_context | 54 |
| public_domain_primary | 52 |
| scholarly_primary | 339 |
| social_or_video_context | 12 |
| source_guide_context | 1189 |
| source_guide_primary | 1343 |
| source_quality_anchor | 162 |
| standard_primary | 928 |

## Hard-Fail Rows

| Path | Line | Claim class | Terms | Fix hint |
|---|---:|---|---|---|
| None | 0 | - | - | - |

## Calibration Rule

Citation presence is necessary but not sufficient. Strong empirical, statistical, performance, governance, safety, formalism, and visual claims must either cite direct support or state a clear boundary that keeps the prose from becoming proof-language.
