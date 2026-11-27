# AGEINT citation provenance evidence

This offline check verifies the citation inventory reported by a retained
AGEINT audit. It compares the [citation guide](../citation_workflow.md) and
the generated bibliography atlas from the same pinned source revision. Both distinguish source-guide references, curated research anchors,
and source-quality anchors.

The [evidence receipt](citation-provenance.json) records the source revision,
file hashes, report timestamp, and selected aggregate values. The September 7,
2026 report counted 1,468 uses of 301 distinct citation keys across 723 source
sections. Its 472 source metadata records comprise 462 research anchors and
10 source-quality anchors. An occurrence counts a use of a key, while a
metadata record describes an entry in the source metadata audit.

## Replay the retained evidence

Use Python 3 and Git in a checkout whose local Git objects contain the
revision and three source files listed in the receipt. From the repository root:

```sh
python3 docs/evidence/replay_citation_provenance.py
```

The replay disables Git's lazy fetching and verifies both Git blob IDs and
SHA-256 digests. It checks that the guide and atlas contain the same three category labels, then compares the selected integer fields and reconciles the
metadata total. A shallow or filtered checkout needs those objects
materialized before an offline replay. The command prints one JSON summary
and does not modify the checkout.

## Isolated render receipt

A separate citation-provenance selection used these aggregates in a
seven-page PDF, HTML, and one category-count figure. The receipt records the
exact [Template revision](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2),
source bundle commit, output hashes, and all nine Stage 04 checks. The
ordinary checkout carries the evidence replay and receipt. The isolated
render source and its PDF and HTML are outside this repository.

Citation presence measures coverage under the retained report's definitions.
It does not establish that a source supports each claim. This guide leaves
the [canonical manuscript source](../manuscript/README.md), the published
edition, and the separate [synthetic assurance example](../offline_assurance.md)
in their existing roles.
