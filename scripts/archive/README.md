# Archived migration scripts

One-time pyfrag-to-subpackage migration tools from May 2026. These scripts are
not part of normal AGEINT builds and are retained for historical reference only.

| Script | Purpose |
| --- | --- |
| `migrate_pyfrag_packages.py` | Convert `.pyfrag` composition to real subpackages |
| `migrate_chapter_profiles.py` | Backfill `content_profile` and `practice_lens` on chapter shards |
| `fix_packages.py` | Repair package imports after subpackage split |
| `fix_part_imports.py` | Normalize `_NN_part.py` import wiring |

Run the canonical build with `uv run python scripts/build_curriculum.py`.
