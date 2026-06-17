## Data lineage registry: source identity, transformations, retention, and review {#sec:data-lineage-registry}

| Object | Lineage field | Quality gate |
|---|---|---|
| Source citation | `ageintNNN`, title, URL, checked date, and source identity status | citation key resolves and reference identity is locked or append-only |
| Verified anchor | lane, tier, verification method, claim scope, stakeholder role, and assurance use | direct official, standards, public-domain, or scholarly URL was reviewed |
| Dataset or scenario | origin, license, sensitivity class, transformations, and retention rule | public, synthetic, owned-lab, or instructor-provided data only |
| Agent transcript | prompt, model context, tool allowlist, budget, reviewer, and blocked actions | no external action, live target, private data, or unsafe cyber-physical step |
| Final artifact | claim ledger, uncertainty note, accessibility status, rights review, and refresh owner | another reviewer can reproduce and challenge the artifact |
