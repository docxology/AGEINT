# Cryptographic Methods {#sec:appendix-cryptographic-methods}

## Cryptographic Methods workbook scope: purpose, safety envelope, and reuse decision

**Navigation.** Parent section: [@sec:appendix-cryptographic-methods].

### Cryptographic Methods operating purpose
Source-item focus: One-Time Pad: Theory and Python Implementation; Signal Protocol and Modern E2E Encryption Architecture. The source-item map preserves the curriculum identity; it does not authorize the source item's operational wording. Use only the offline substitutions below: no live queries, credentials, private records, external code execution, profiling, persuasion delivery, or cyber-physical actions.

Use the claim record and eight-step analytic procedure in [@sec:analytic-workflow], not a second local evidence schema. All inputs below are invented classroom records. Worked outputs and negative-control results are authored expectations, not executed tests, empirical findings, or evidence that a named framework is secure or effective.

## Cryptographic standards boundary

Cryptographic properties need their own standards evidence: encryption, hashing, digital signatures, and key lifecycle are distinct subjects [@official_nist_fips_197_aes]; [@official_nist_fips_180_4_shs]; [@official_nist_fips_186_5_dss]; [@official_nist_sp_800_57pt1r5_key_management]. These sources do not establish the truth of a signed statement or the safety of an entire messaging system. See [@fig:appendix-crypto-assurance-methods].

**Input.** Fictional message E1 says 'the archive is closed on day 12'; E2 corrects it to 'open on day 12'. An instructor-supplied card labels E1 `signature valid under key K` and E2 `unsigned`; another card says the holder-to-key binding is unverified. These are assumed fixture labels, not actual cryptographic verification results.

1. Make a property ledger: encryption concerns confidentiality under specified assumptions; a digest comparison concerns byte consistency; signature verification concerns a signature/message/key relation. Separately record key identity, authorization, freshness, and statement truth as unresolved unless supported.
2. Treat the one-time-pad source item as an assumptions worksheet: uniform secret independent key, at least message length, used once. Do not infer those conditions from the algorithm's name or implement a communications channel.
3. Review Signal/PGP source motifs as architecture and lifecycle questions: which property is claimed, under what key/custody assumptions, and what direct source supports it? An AES standard alone is not evidence for an application's end-to-end security.
4. Compare E1 and E2 for substantive evidence and dates independently of signature status. Record the supplied signature label without upgrading E1 to a true or authorized notice.
5. Keep steganography and dead-drop items as historical/detection-literacy review only; no embedding, concealment, transmission, live keys, or operational secrecy procedure [@ageint027]; [@ageint028].

**Example output.** `E1: supplied signature-status=valid-under-K; holder binding=unknown; content truth=disputed by E2; authorized notice=not established; disposition=hold`. `E2: unsigned` does not by itself mean false.

**Expected negative-control result.** Give a false fixture statement the same 'valid signature' label: its truth status must not improve. Change E1's bytes while retaining its old verification card: mark the card inapplicable until rechecked, rather than asserting a cryptographic failure was observed.

**Reuse disposition and applicability.** Reuse the property ledger if learners keep integrity, authenticity assumptions, confidentiality, and truth separate. Record provenance of fixture labels and retention/release decisions; key-management and vendor forms become applicable only for a separately authorized implementation, not because a paper card names a key. Refresh on the relevant standard or architecture version.

### Cryptographic Methods shared forms and local applicability record
Complete one local record: `packet/version; applicable forms and reason; not-applicable forms and reason; missing evidence; reviewer; disposition; refresh trigger`. The workbook's applicability note is a starting point, not approval. Never replace a missing review with a bare 'N/A'.

For provenance and documentation, use [@sec:source-lane-map], [@sec:data-lineage-registry], and [@sec:model-and-dataset-documentation-card]. For communication and handling, use [@sec:transparency-and-communication-notice] and [@sec:records-retention-and-audit-trail].

For rights, access, and tool changes, use [@sec:hria-and-dpia-worksheet], [@sec:accessibility-and-udl-review], [@sec:learner-support-and-accommodation-plan], and [@sec:procurement-and-vendor-oversight]. For reuse or exceptions, use [@sec:release-and-change-control-gate] and [@sec:risk-exception-and-acceptance-memo].

For teaching and revision, use [@sec:assessment-integrity-protocol], [@sec:instructor-question-bank], [@sec:adversarial-assurance-cycle], and [@sec:remediation-backlog]. Apply the competency and answer-quality rubrics in [@sec:method-assurance-reference]; retain the relevant local evidence rather than copying every shared table into the packet.

### Cryptographic Methods visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-crypto-assurance-methods] and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-autogen-and-mcp-patterns], [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

![The named standards address distinct properties under specific algorithm, implementation, and trust assumptions. AES alone does not establish authenticated messaging; a hash needs a trusted reference; a signature needs valid verification and trusted identity/key binding. Record failed or unavailable checks rather than declaring a message verified. Classroom controls include an altered record with an altered untrusted checksum and a validly signed false statement: cryptographic validity does not settle content truth.](../../figures/mermaid/appendix-crypto-assurance-methods.png){#fig:appendix-crypto-assurance-methods}

### Cryptographic Methods runtime item map and source roster: generated rows and citation support

| Source item / safe study title | Provenance status | Citation context |
|---|---|---|
| E.1 One-Time Pad: Theory and Python Implementation | no blocked motif; source title used verbatim | - |
| E.2 Signal Protocol and Modern E2E Encryption Architecture | no blocked motif; source title used verbatim | - |
| E.3 PGP/GPG for Operational Security: Key Management | no blocked motif; source title used verbatim | - |
| Steganography detection-literacy and communications-security review | E.4 retained for audit; operational wording transformed | [@ageint028] |
| E.5 Digital Dead Drop Implementation: Email/PasteBin/S3 | no blocked motif; source title used verbatim | - |
