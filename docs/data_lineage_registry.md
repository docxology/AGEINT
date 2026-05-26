# Data Lineage Registry

The data lineage registry keeps AGEINT generated chapters and appendices
auditable. It appears in every chapter and is expanded in the source
verification and claim-ledger workflow.

## Registry Objects

- Source citation: `ageintNNN`, title, URL, checked date, and lock status.
- Verified anchor: lane, tier, verification method, claim scope, stakeholder
  role, assurance use, and rights dimension.
- Dataset or scenario: origin, license, sensitivity class, transformations, and
  retention rule.
- Agent transcript: prompt, model context, tool allowlist, budget, reviewer, and
  blocked actions.
- Final artifact: claim ledger, uncertainty note, accessibility status, rights
  review, and refresh owner.

## Source Rules

The source identity lock protects `ageint001` through `ageint231`; current
append-only references extend through `ageint312`. Generated output remains a
rebuild product and should not be edited by hand.

## Safety Boundary

Lineage records may describe blocked unsafe motifs for audit purposes. They
must not include private data, live system secrets, credential material,
targeting records, or deployable operational instructions.
