# AGEINT Current Artifact Evidence

| Measure | Value |
|---|---:|
| OK | true |
| Generated at | 2026-06-17T04:16:58+00:00 |
| Generated Markdown files | 330 |
| Generated citation occurrences | 16604 |
| Thin claim-bearing files | 0 |
| Single-family claim-bearing files | 6 |
| SAT method contract | true |
| Analysis validation contract | true |
| Analysis validation lane contract | true |
| Analysis validation family coverage | true |
| Source metadata explicit | true |
| Source metadata rows | 472 |
| Source metadata fallback rows | 0 |
| Blank source lanes | 0 |
| Blank source tiers | 0 |
| Source refresh due pass | true |
| Source refresh due/stale rows | 0 |
| Source refresh missing checked dates | 0 |
| Agency source coverage pass | true |
| New official US IC anchors | 56 |
| Agency-source unrouted rows | 0 |
| Agency-source missing metadata | 0 |
| Claim calibration pass | true |
| Claim-calibration candidate rows | 9107 |
| Claim-calibration hard fails | 0 |
| Claim-calibration review warnings | 5129 |
| Reference quality pass | true |
| Reference-quality issue rows | 0 |
| Generic detail-heading issues | 0 |
| Citation-context issues | 0 |
| Source sections | 723 |
| Zero-citation source sections | 0 |
| Registered figures | 177 |
| Figure quality pass | true |
| PDF pages | 1858 |
| PDF URI links | 6289 |
| Bad PDF link targets | 0 |

## Checks

| Check | Pass |
|---|---:|
| generated output fresh | true |
| rendered references resolve | true |
| reference quality ok | true |
| stale output scans clean | true |
| pdf quality ok | true |
| figure quality ok | true |
| citation source sections covered | true |
| scholarship quality ok | true |
| source metadata ok | true |
| source refresh due ok | true |
| agency source coverage ok | true |
| claim calibration ok | true |

## False-Certification Control

**Scenario.** A reviewer trusts a copied PDF, citation count, current-evidence note, or green local report without proving that all registered audits passed against the same rebuilt artifact set.

**Negative control.** Touch a source-owned route, template, or figure file after build; the evidence manifest must fail freshness. Insert a generated link to a local .md or .markdown target; rendered-reference evidence must fail. Restore a generic generated scaffold heading, incomplete lesson cross-link, or citation-only table row. Restore the old source-section coverage table header or stale scholarly source phrase. Make the PDF older than the combined manuscript or add a file: PDF target. Remove figure alt text, provenance, or readable PNG metadata from a registered figure. Collapse a source section to zero citations while retaining claim-bearing text. Remove the SAT figure reference, analysis-validation matrix reference, or one required claim class from orientation prose. Add one curated source-anchor row with an empty source_lane or source_tier. Set checked_as_of blank or past the allowed cadence for one source row. Add a new official US IC anchor without source_agency, source_pack, or pack routing. Add an unsupported measured-performance, p-value, or proof-language claim backed only by weak context.

## Audit Contract Negative Controls

| Contract | Check | Negative control |
|---|---|---|
| `generated_output_freshness` | `generated_output_fresh` | Touch a source-owned route, template, or figure file after build; the evidence manifest must fail freshness. |
| `rendered_reference_resolution` | `rendered_references_resolve` | Insert a generated link to a local .md or .markdown target; rendered-reference evidence must fail. |
| `reference_quality` | `reference_quality_ok` | Restore a generic generated scaffold heading, incomplete lesson cross-link, or citation-only table row. |
| `stale_output_scan` | `stale_output_scans_clean` | Restore the old source-section coverage table header or stale scholarly source phrase. |
| `pdf_quality` | `pdf_quality_ok` | Make the PDF older than the combined manuscript or add a file: PDF target. |
| `figure_quality` | `figure_quality_ok` | Remove figure alt text, provenance, or readable PNG metadata from a registered figure. |
| `citation_source_section_coverage` | `citation_source_sections_covered` | Collapse a source section to zero citations while retaining claim-bearing text. |
| `scholarship_quality` | `scholarship_quality_ok` | Remove the SAT figure reference, analysis-validation matrix reference, or one required claim class from orientation prose. |
| `source_metadata` | `source_metadata_ok` | Add one curated source-anchor row with an empty source_lane or source_tier. |
| `source_refresh_due` | `source_refresh_due_ok` | Set checked_as_of blank or past the allowed cadence for one source row. |
| `agency_source_coverage` | `agency_source_coverage_ok` | Add a new official US IC anchor without source_agency, source_pack, or pack routing. |
| `claim_calibration` | `claim_calibration_ok` | Add an unsupported measured-performance, p-value, or proof-language claim backed only by weak context. |
