## Verifier-first artifact evidence: build freshness, audits, and negative controls {#sec:verifier-first-artifact-evidence}

AGEINT uses the RedTeam rule that a green validator is evidence only after the
validator has been challenged. The artifact-evidence control loop in
[@fig:ageint-artifact-evidence-control-loop] binds source-owned curriculum
inputs, generated manuscript sections, citation inventories, figure metadata,
PDF annotations, and current evidence reports into one falsifiable chain. This
keeps scholarship, visual assets, and render validation in the same audit
surface: a stale PDF, a local Markdown-file link, an uncovered source section,
or a figure-registry mismatch must fail the evidence manifest before a
maintainer can treat the render as ready. The same stance follows the
evaluation and red-team assurance guidance already encoded in the bibliography
atlas: adversarial testing is a scoped assurance method, not proof of universal
safety or permission to run live operations
[@official_cisa_ai_red_teaming_tev];
[@official_nist_aria_pilot_evaluation_report];
[@official_nist_ai_600_1_generative_ai_profile].
