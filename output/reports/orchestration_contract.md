# AGEINT Contract Map

| Measure | Value |
|---|---:|
| OK | true |
| Pipeline stages | 8 |
| Audit contracts | 12 |
| Source-pack registries | 2 |
| Source-pack issues | 0 |
| Mermaid diagram types | 6 |

## Pipeline Contract

# AGEINT Orchestration Contract

| Measure | Value |
|---|---:|
| Registered stages | 8 |
| Source freshness roots | 15 |
| Output sentinels | 9 |
| Missing output sentinels | 0 |

## Pipeline Stages

| Stage | Purpose | Gate | Failure mode |
|---|---|---|---|
| `source_validation` | Validate declarative curriculum, route, source, and template inputs before rendering. | `validate_declarative_tables` | A malformed route table or source surface reaches manuscript rendering. |
| `curriculum_build` | Load the sharded curriculum spine and optional guide source into the runtime curriculum model. | `curriculum_stats_and_identity_tests` | Generated paths, labels, or counts no longer match the source spine. |
| `template_library` | Optionally regenerate neutral source templates without hard-coding generated chapter data. | `explicit_regeneration_flag` | Reusable templates drift into chapter-specific source text. |
| `variables_and_bibliography` | Refresh manuscript variables plus source and output BibTeX files from current references. | `manuscript_variable_and_reference_tests` | Counts, citation keys, or bibliography shards certify stale source metadata. |
| `figures` | Render Mermaid, Python, historical, and synthetic figures with registry metadata. | `figure_registry_and_quality_tests` | A figure is decorative, inaccessible, stale, or rendered with unsupported chart semantics. |
| `manuscript_render` | Render source-owned manifest sections into generated Markdown under output/manuscript. | `manifest_inventory_reader_quality_tests` | Generated prose, headings, citations, or cross-references drift from the manifest contract. |
| `evidence_transit` | Render the frontmatter evidence-transit figure from current curriculum and artifact counts. | `frontmatter_transit_figure_tests` | Frontmatter evidence counts diverge from the generated manuscript and figure registry. |
| `artifact_reports` | Bind current outputs to fail-closed audit, source, figure, PDF, and readiness evidence. | `artifact_evidence_and_publication_readiness_tests` | A stale or partial artifact is certified as locally ready. |

## Output Sentinels

| Sentinel |
|---|
| `data/curriculum/metadata.json` |
| `data/curriculum_outline.json` |
| `data/manuscript_variables.json` |
| `manuscript/references-source-guide-001-050.bib` |
| `figures/figure_registry.json` |
| `figures/visual_quality_audit.json` |
| `figures/cover/ageint-cover-synthesis.png` |
| `manuscript/README.md` |
| `figures/frontmatter/ageint-evidence-transit-map.png` |

## Audit Contracts

| Contract | Check | Reports | Negative control |
|---|---|---|---|
| `generated_output_freshness` | `generated_output_fresh` | `output/reports/current_artifact_evidence.json` | Touch a source-owned route, template, or figure file after build; the evidence manifest must fail freshness. |
| `rendered_reference_resolution` | `rendered_references_resolve` | `output/reports/current_artifact_evidence.json` | Insert a generated link to a local .md or .markdown target; rendered-reference evidence must fail. |
| `reference_quality` | `reference_quality_ok` | `output/reports/reference_quality.json`, `output/reports/reference_quality.md` | Restore a generic generated scaffold heading, incomplete lesson cross-link, or citation-only table row. |
| `stale_output_scan` | `stale_output_scans_clean` | `output/reports/current_artifact_evidence.json` | Restore the old source-section coverage table header or stale scholarly source phrase. |
| `pdf_quality` | `pdf_quality_ok` | `output/reports/current_artifact_evidence.json`, `output/reports/pdf_quality.json` | Make the PDF older than the combined manuscript or add a file: PDF target. |
| `figure_quality` | `figure_quality_ok` | `output/figures/visual_quality_audit.json` | Remove figure alt text, provenance, or readable PNG metadata from a registered figure. |
| `citation_source_section_coverage` | `citation_source_sections_covered` | `output/reports/current_artifact_evidence.json` | Collapse a source section to zero citations while retaining claim-bearing text. |
| `scholarship_quality` | `scholarship_quality_ok` | `output/reports/scholarship_quality.json`, `output/reports/scholarship_quality.md` | Remove the SAT figure reference, analysis-validation matrix reference, or one required claim class from orientation prose. |
| `source_metadata` | `source_metadata_ok` | `output/reports/source_metadata.json`, `output/reports/source_metadata.md` | Add one curated source-anchor row with an empty source_lane or source_tier. |
| `source_refresh_due` | `source_refresh_due_ok` | `output/reports/source_refresh_due.json`, `output/reports/source_refresh_due.md` | Set checked_as_of blank or past the allowed cadence for one source row. |
| `agency_source_coverage` | `agency_source_coverage_ok` | `output/reports/agency_source_coverage.json`, `output/reports/agency_source_coverage.md` | Add a new official US IC anchor without source_agency, source_pack, or pack routing. |
| `claim_calibration` | `claim_calibration_ok` | `output/reports/claim_calibration.json`, `output/reports/claim_calibration.md` | Add an unsupported measured-performance, p-value, or proof-language claim backed only by weak context. |

## Source-Pack Contracts

| Class | Packs | Routes | Issues |
|---|---:|---:|---:|
| `agency` | 10 | 0 | 0 |
| `research` | 5 | 14 | 0 |

## Mermaid Diagram Types

| Type | Purpose | Reader detail required |
|---|---|---:|
| `flowchart` | Structural maps, routing diagrams, and governance boundary flows. | false |
| `stateDiagram-v2` | State, recovery, and circuit-breaker transitions. | true |
| `sequenceDiagram` | Actor interactions, evidence handoffs, and verification exchanges. | true |
| `journey` | Reviewer and learner experience paths across staged work. | true |
| `timeline` | Temporal degradation, incident, and refresh sequences. | true |
| `quadrantChart` | Two-axis evidence-fit and claim-risk classification maps. | true |
