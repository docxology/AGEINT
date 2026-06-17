## Scholarship and governance stance: source posture, claim limits, and public-readiness boundary {#sec:scholarship-and-governance-stance}

AGEINT treats agentic intelligence as a governed socio-technical practice, not
as a bag of prompts or autonomous tricks. The curriculum therefore keeps AI
agent evaluation, identity, authorization, secure tool use, structured analytic
tradecraft, cognitive security, OSINT/GEOINT integrity, and ICS/OT safety in
one source-backed frame. Each source anchor has a curriculum role, a domain,
and a provenance type so readers can distinguish law, standards, official
guidance, public-domain historical material, scholarly synthesis, and weaker
practitioner or vendor context. Unless a section cites an empirical study or
evaluation source for a narrower point, AGEINT language should be read as
proposed design guidance and an assurance framework rather than measured
performance evidence. Technical and theoretical analogies, including
active-inference material, remain bounded by their direct domain sources and do
not become deployment evidence without separate evaluation support.

The same stance now has a machine-checkable extension. Citation presence is
necessary but not sufficient for AGEINT scholarship, so the generated manuscript
is checked for source-family mix, uncited claim-bearing sections, thin
claim-bearing support, and sections whose support comes from only one broad
family. The audit distinguishes hard failures from review warnings: a
claim-bearing overview, lesson, worked example, architecture source section,
research-governance section, assessment review, or unit introduction with zero
or one unique citation fails the current artifact evidence; a section with
multiple citations from one source family is reported as a review target for
future triangulation. The control surface is summarized in
[@fig:ageint-scholarship-triangulation-map], and the machine-readable companion
report is written to `output/reports/scholarship_quality.json` during the
current-evidence pass. This keeps source-guide inheritance visible while still
preferring official, standards, law/policy, public-domain, and scholarly anchors
whenever a section makes a stronger governance, technical, or empirical claim
[@scholarly_rethlefsen_2021_prisma_s]; [@official_nist_ai_rmf];
[@official_nist_ai_600_1].

Claim calibration sits beside that scholarship audit. The source-strength layer
classifies source-guide rows and curated anchors by whether they can carry a
bounded claim directly or only provide context. Weak source-guide context,
vendor/practitioner commentary, social/video rows, and mirror/copy rows cannot
alone support empirical performance, statistical, governance-authority, safety,
or formalism claims. The current report is written to
`output/reports/claim_calibration.json` and `.md`, and the unified artifact
evidence manifest exposes the result as `claim_calibration_ok`.

Analysis validation adds the reader-facing disposition layer, summarized as a
claim-class-to-question matrix in [@sec:analysis-validation-protocol] and
[@fig:ageint-analysis-validation-matrix]; that matrix is the boundary on what the
manuscript can honestly say. This is why the artifact-evidence manifest records
both positive counts and false-certification controls.
