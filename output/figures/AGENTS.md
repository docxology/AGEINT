# AGENTS.md - AGEINT Figures

Generated figure assets are local, registry-backed, and defensive. Do not edit PNGs by hand; update `src/figures/` or curriculum data, then rebuild so hashes, captions, alt text, long descriptions, labels, embedded PNG metadata, and manuscript references stay aligned.

Mermaid diagrams must be kept as local `.mmd` sources paired with square-normalized PNGs. Python, historical, and synthetic assets should also stay roughly square after rendering; tests enforce readable PNGs and aspect-ratio bounds.

Do not add real targets, operational screenshots, exploit interfaces, official logos, images of private people, or unsafe cyber-physical scenes. Historical imagery must retain public-domain provenance in `figure_registry.json`.
