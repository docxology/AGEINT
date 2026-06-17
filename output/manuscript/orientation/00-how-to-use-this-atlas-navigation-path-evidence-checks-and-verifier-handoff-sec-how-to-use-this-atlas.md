# Curriculum Orientation: reader paths, evidence maps, and safety gates {#sec:curriculum_orientation}

AGEINT (Agentic Intelligence) is a curriculum-and-assurance atlas for teaching
how AI agents can *assist* intelligence analysis without ever being trusted to
run it unsupervised. It is written for three readers: an **instructor**
assembling a defensible course, a **learner** building analytic habits on safe
practice material, and an **assurance reviewer** checking that every claim can be
traced back to a real source. Nothing here is operational — every exercise uses
synthetic or public material, and every claim is built to be challenged rather
than believed.

Read it as a map, not a textbook to read front to back: [@sec:curriculum-map]
lets you choose a domain part, [@sec:reader-paths] gives each reader a fast path,
and [@sec:safety-rail] states what the atlas refuses to teach.

> **For maintainers.** This page is generated. The source templates under
> `manuscript/templates/` keep guide-derived values — titles, labels, counts,
> source spines, semantic paths, and bibliography rows — as neutral tokens; the
> build resolves them from `data/curriculum/` into the rendered manuscript in
> `output/manuscript/`. Edit the template, not the rendered output.

The rest of this orientation is a toolkit for navigating that map; the next
section shows the exact path.

## How to use this atlas: navigation path, evidence checks, and verifier handoff {#sec:how-to-use-this-atlas}

Read AGEINT as a navigable curriculum-and-assurance atlas rather than a linear
textbook or empirical evaluation report. Start with [@sec:curriculum-map] and
[@fig:ageint-curriculum-map] to choose the part, open the linked part
introduction to see the module sequence, then use each chapter overview for the
figures, source lane, and assessment artifact that matter for the current
decision. Keep [@sec:bibliography_atlas] open when checking a claim, because it
preserves source identity, provenance type, source tier, and refresh context in
one place.

Use the first pages as signposts, not as a preface to skip. The handoff is
intentionally explicit and always moves in the same direction:

domain part -> module overview -> practice studio -> evidence contract ->
governance boundary -> assessment route -> bibliography/source lane ->
verifier reports.

Work the table below in order: orient, then match each claim to its evidence,
then verify before trusting anything.

| Step | Where to go | Why this step matters |
|---|---|---|
| Start here | [@sec:curriculum-map], [@sec:synthetic-analytic-tradecraft-thesis], and [@sec:reader-paths] | Choose a domain part, name the Synthetic Analytic Tradecraft contract, and decide which reader path governs the next move. |
| Then check | [@sec:analysis-validation-protocol], [@sec:source-lane-map], and [@sec:bibliography_atlas] | Match the claim class to evidence, lane, citation identity, and refresh duty before treating prose or figures as support. |
| Before you trust | [@sec:safe-substitution-matrix], [@sec:orientation-figures-and-course-links], and [@sec:method-assurance-reference] | Confirm risky motifs were converted to bounded artifacts, figures carry their limits, and verifier reports agree with the rendered manuscript. |
| Govern and assure | [@sec:hria-and-dpia-worksheet], [@sec:adversarial-assurance-cycle], [@sec:model-and-dataset-documentation-card], and [@sec:records-retention-and-audit-trail] | Bind rights impact, red-team challenge, documentation provenance, and retention duty to each reusable artifact before it leaves the course. |

Claim classes are separated at source-selection time. Governance claims,
technical and theoretical claims, empirical capability claims, and
source-construction claims each need a matching evidence type; the shared method
reference records the PRISMA-S-inspired source-reporting fields used when a
search or discovery process supports manuscript content
[@scholarly_rethlefsen_2021_prisma_s].

The opening route visual turns the atlas handoff into a concrete reader choice: select the role, keep the evidence trace, and move to the next section with the right verifier question already named. See [@fig:ageint-reader-route-compass].

![Opening navigation compass for the AGEINT orientation. It separates the instructor, learner, assurance reviewer, and maintainer routes and pairs each with the evidence trace that should survive the next reading move, so a reader can choose a path and know what to carry into the following section. It is navigation support, not a learning-outcome or performance claim.](../../figures/python/ageint-reader-route-compass.png){#fig:ageint-reader-route-compass}
