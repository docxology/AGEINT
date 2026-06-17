## Analysis validation protocol: claim classes, evidence packets, and failure modes {#sec:analysis-validation-protocol}

The manuscript now treats analysis validation as a reader-facing method, not a
private build habit. Each major claim class must name the evidence packet that
would make it reviewable, the validation question a reviewer should ask, and
the failure mode that would force warning or remediation. The analysis
validation matrix [@fig:ageint-analysis-validation-matrix] is the compact visual
form of that protocol: design guidance needs a source family and caveat;
empirical or evaluation claims need a study, metric, or benchmark; governance
claims need law, standard, or rights-impact support; figure claims need registry
text, rendered pixels, and link-safe PDF output; artifact-readiness claims need
fresh builds and current audits; reviewer dispositions need a task ledger and
negative control.

The claim-calibration verifier adds the machine-checkable edge to that protocol
[@fig:ageint-claim-calibration-and-visual-semantics]. Artifact telemetry such as
citation counts, figure counts, page counts, link counts, and validator pass
states is useful readiness evidence, but it is not a statistical result,
learning-outcome estimate, operational-performance benchmark, or universal
safety claim. The audit therefore fails unsupported proof-language,
measured-performance claims, p-value or significance language, and decorative
formalisms without direct support and limitation text, while allowing explicit
boundary language and misconception checks that warn the reader what a source
cannot establish.

| Claim class | Validation question | Required evidence | Failure mode |
|---|---|---|---|
| Design guidance | Is the claim framed as proposed guidance rather than measured performance? | source-family support, caveat, and bounded conclusion | architecture prose is promoted into empirical proof |
| Empirical or evaluation claim | Does a cited study, metric, benchmark, or evaluation source directly support the claim? | method source, limitation note, and refresh trigger | measured language appears without direct evaluation evidence |
| Governance or rights claim | Which law, standard, public guidance, or rights-impact source constrains the advice? | source lane, affected group, owner, residual risk | compliance language appears as unsupported assurance |
| Figure or visualization claim | Does the visual carry readable text, alt text, provenance, and an inspectable source section? | registry row, PNG metadata, caption, long description | a figure works only as decoration or inaccessible evidence |
| Artifact readiness claim | Are manuscript, citations, figures, references, and PDF links from the same rebuild? | artifact-evidence manifest, rendered-reference audit, PDF audit | stale output or Markdown-file links certify as ready |
| Reviewer disposition | What would make this row pass, warn, fail, or reopen? | negative control, closure evidence, task owner | a green check hides the decision rule |

The assurance cockpit visual summarizes how a reader should interpret local build telemetry: useful for routing review effort, but bounded by the generated audits that carry the authoritative pass, warn, or block state. See [@fig:ageint-assurance-cockpit].

![Audit-tile orientation cockpit for local readiness. It groups build freshness, reference quality, source metadata, refresh posture, figure quality, and the publication-readiness boundary into reader-facing tiles that route review effort to the right verifier. The tiles are schematic orientation only; authoritative status — the pass, warn, or block state — lives in the generated audits, not in this figure.](../../figures/python/ageint-assurance-cockpit.png){#fig:ageint-assurance-cockpit}
