# AGEINT Claim Calibration

| Measure | Value |
|---|---:|
| OK | true |
| Generated at | 2026-07-11T02:22:24+00:00 |
| Candidate rows | 9111 |
| Hard-fail rows | 0 |
| Review-warning rows | 5133 |
| Boundary-allowed rows | 482 |

## Claim Class Distribution

| Claim class | Rows |
|---|---:|
| artifact_readiness | 286 |
| empirical_or_evaluation | 986 |
| figure_or_visualization | 459 |
| formalism_or_statistical_expression | 2 |
| governance_or_rights | 3090 |
| safety_or_assurance | 4288 |

## Source Support Distribution

| Source support distribution | Mentions |
|---|---:|
| curated_context | 12 |
| law_policy_primary | 19 |
| mirror_or_copy_context | 36 |
| official_primary | 1474 |
| practitioner_or_vendor_context | 54 |
| public_domain_primary | 166 |
| scholarly_primary | 371 |
| social_or_video_context | 13 |
| source_guide_context | 255 |
| source_guide_primary | 2208 |
| source_quality_anchor | 504 |
| standard_primary | 952 |

## Hard-Fail Rows

| Path | Line | Claim class | Terms | Fix hint |
|---|---:|---|---|---|
| None | 0 | - | - | - |

## Calibration Rule

Citation presence is necessary but not sufficient. Strong empirical, statistical, performance, governance, safety, formalism, and visual claims must either cite direct support or state a clear boundary that keeps the prose from becoming proof-language.
