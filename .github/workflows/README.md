# AGEINT workflows

| Workflow | Scope |
| --- | --- |
| `ci.yml` | Required complete SDK verification plus locked lint and separately named limited standalone Python checks |
| `manuscript.yml` | Reusable complete build/test/render/audit gate; also manual and weekly |
| `release.yml` | Manual-only new stable release, after fresh complete verification of exact current main |
| `source-freshness.yml` | Source refresh-due audits |

Complete verification uses the genuine SDK `v5.1.0` tag, Python 3.14, frozen
SDK dev/rendering dependencies, pinned SDK Mermaid/browser/document setup and
the SDK's canonical native renderer. The standalone 84% compatibility jobs are
not release acceptance; the complete gate requires at least 90% coverage and
blocking PDF, HTML, artifact and publication-readiness checks, including the
actually-executed all-resource parent guard. Missing SDK tags and failed setup,
builds or audits stop the job. Old outputs are never restored after failure.

The source manuscript config must select `render.html.asset_mode: local` for
self-contained readers. The reader ZIP retains `web/` (canonical `index.html`
and local browser assets) beside `figures/`, preserving `../figures/` links.
Only a successful complete run uploads verified readers, evidence, source/SDK
identity and SHA-256 checksums.
Serve the extracted reader bundle root over local HTTP, then visit
`http://localhost:8000/web/index.html`; do not serve only `web/`. Browser features
are not all guaranteed under `file://`. External scholarly URLs remain
user-clicked references, not remotely fetched runtime assets.

```bash
unzip AGEINT-reader.zip -d reader
python -m http.server 8000 --directory reader --bind 127.0.0.1
```

## Maintainer commands

After the SDK tag genuinely exists and satisfies its own acceptance, and the
AGEINT release changes are committed on main:

```bash
gh workflow run manuscript.yml --repo docxology/AGEINT --ref main
gh run list --repo docxology/AGEINT --workflow manuscript.yml --limit 5
gh run watch <verification-run-id> --repo docxology/AGEINT --exit-status
gh run download <verification-run-id> --repo docxology/AGEINT --dir verified
(cd verified/verified-ageint-* && shasum -a 256 --check SHA256SUMS)
```
Before the SDK release exists, development verification may explicitly select
one immutable candidate commit (set `SDK_CANDIDATE_SHA` to its full 40-hex SHA).
This retains every complete acceptance gate; it is never an implicit fallback
or publication authorization:

```bash
gh workflow run manuscript.yml --repo docxology/AGEINT --ref main -f "sdk-candidate=$SDK_CANDIDATE_SHA"
```

Normal CI, scheduled and release runs authenticate the published stable SDK
`v5.1.0` release/tag. Candidate artifacts identify their actual SDK SHA/version
and cannot be used by `release.yml`.

Run the manual release only under explicit publication authorization:

```bash
gh workflow run release.yml --repo docxology/AGEINT --ref main -f tag=v0.2.0
gh run list --repo docxology/AGEINT --workflow release.yml --limit 5
gh run watch <release-run-id> --repo docxology/AGEINT --exit-status
```

The release dispatch does not trust the prior manual/ordinary-CI result: it runs
the complete reusable gate again on its exact main Source and checks the tag
against the read-only metadata CLI. Main must still match immediately before
create-only tag publication. Existing tags/releases are refused, including an
orphaned tag left by a failed release upload. No automatic deletion, movement or
overwrite is attempted; investigate failures before any separately authorized
recovery.
