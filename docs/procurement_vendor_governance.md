# Procurement Vendor Governance: tool oversight, revocation, and vendor evidence

AGEINT uses procurement/vendor governance when a chapter mentions a tool,
dataset, model, platform, service, or external dependency. The generated
**Governance, rights, and assurance** section carries procurement/vendor
monitoring so tool adoption stays reviewable inside the local lifecycle project
checkout. This copy currently lives at `projects/working/AGEINT`; parent-template
workflows may link it as `projects/active/AGEINT` or `projects/AGEINT` during
promotion or hot-seat runs.

## Oversight loop: evaluate, approve, monitor, replace, and document tools

- Need and authority: document why the capability is needed and who approved it.
- Vendor transparency: identify provider, subcontractors, data use, logs,
  accessibility duties, and conflicts of interest.
- Evaluation criteria: score privacy, accessibility, security, provenance,
  reversibility, and assessment integrity before selection.
- Contract controls: require logging, deletion, audit, incident, accessibility,
  and exit clauses.
- Lifecycle monitoring: refresh before renewal or classroom reuse.

## Source rules: procurement anchors and vendor-risk support

Procurement references are append-only after the existing source guide and are
directly verified. Guide references `ageint278` and `ageint279` cover OECD
public procurement and the Open Contracting Data Standard. Curated anchors add
OMB M-25-22 for federal AI acquisition, CISA Secure by Demand for OT product
selection, CISA AI data-security best practices, and CISA secure AI deployment.
The `ageint001` through `ageint231` identity lock remains unchanged.

## Safety boundary: synthetic substitutes and no unreviewed external action

Vendor review is a governance exercise. It must not become live vendor probing,
credential testing, private-data collection, or production-system action.
