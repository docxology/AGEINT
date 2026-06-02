# Archived migration scripts

One-time pyfrag-to-subpackage migration tools from May 2026. These scripts are
not part of normal AGEINT builds and are retained for historical reference only.
Part-import wiring uses explicit cross-part imports in each sharded package under
`src/`; `_package_loader.merge_part_modules()` was retired in 2026-06. Do not
re-run the removed `fix_part_imports.py` migrator.

| Script | Purpose |
| --- | --- |
| `migrate_pyfrag_packages.py` | Convert `.pyfrag` composition to real subpackages |
| `migrate_chapter_profiles.py` | Backfill `content_profile` and `practice_lens` on chapter shards |
| `fix_packages.py` | Repair package imports after subpackage split |

Run the canonical build with `uv run python scripts/build_curriculum.py`.
