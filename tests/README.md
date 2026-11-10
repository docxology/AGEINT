# AGEINT Tests

This folder contains AGEINT parser, template, manifest, figure-registry, build, and manuscript-integrity tests.

- Owner: AGEINT quality gates.
- Status: manual tests.
- Source of truth: project behavior and the token-injected architecture.
- Run: `python -m pytest tests/ --cov=src --cov-fail-under=90` from AGEINT in the same prepared SDK environment as the [full workflow](../README.md#commands).
- Safety: tests should catch unsafe operational framing and unresolved generated tokens.

`built_output` reads existing artifacts without generating or repairing them.
Build a new edition explicitly before validation; retain genuine missing,
stale-output, navigation and typed-count failures in an existing publication.

The suite uses real project inputs. It validates guide parsing, source-anchor
BibTeX generation, neutral template behavior, semantic output ordering,
registry-backed figure insertion, readable square figure assets, generated
folder docs, source identity stability, source-lane metadata, generated v2
chapter/appendix structures, deep expansion sections, accessibility/rights
review, procurement/vendor governance, agent incident response, adversarial
assurance, and the defensive/evidence-bounded boundary.
