"""Replay the aggregate citation evidence using three pinned local Git blobs."""

import hashlib
import json
import os
from pathlib import Path
import subprocess


REPOSITORY = Path(__file__).resolve().parents[2]
RECEIPT = Path(__file__).with_name("citation-provenance.json")
WORKFLOW = "docs/citation_workflow.md"
ATLAS = (
    "output/manuscript/appendices/bibliography-atlas/"
    "03-citation-workflow-and-source-section-coverage.md"
)
REPORT = "output/reports/current_artifact_evidence.json"


def replay() -> dict:
    evidence = json.loads(RECEIPT.read_text(encoding="utf-8"))["source_evidence"]
    materials = {entry["path"]: entry for entry in evidence["materials"]}
    if materials.keys() != {WORKFLOW, ATLAS, REPORT}:
        raise ValueError("Unexpected source roster in the citation receipt")
    blobs = {}
    for name, entry in materials.items():
        blob = subprocess.check_output(
            ["git", "cat-file", "blob", f"{evidence['commit']}:{name}"],
            cwd=REPOSITORY,
            env={**os.environ, "GIT_NO_LAZY_FETCH": "1"},
        )
        header = f"blob {len(blob)}\0".encode()
        if hashlib.sha1(header + blob).hexdigest() != entry["git_blob"]:
            raise ValueError(f"Git blob mismatch for {name}")
        if hashlib.sha256(blob).hexdigest() != entry["sha256"]:
            raise ValueError(f"SHA-256 mismatch for {name}")
        blobs[name] = blob

    roles = (
        b"Source-guide reference",
        b"Curated research anchor",
        b"Source-quality anchor",
    )
    if any(role not in blobs[path] for path in (WORKFLOW, ATLAS) for role in roles):
        raise ValueError("The guide and generated atlas disagree on citation roles")

    report = json.loads(blobs[REPORT])
    fields = {
        "source": report["citations"],
        "generated": report["citations"],
        "metadata": report["source_metadata"]["summary"],
    }
    if report["generated_at"] != evidence["report_generated_at"]:
        raise ValueError("The report timestamp differs from the recorded snapshot")

    observed = {}
    for group, source in fields.items():
        values = {key: source[key] for key in evidence[group]}
        if any(type(value) is not int for value in values.values()):
            raise ValueError(f"Non-integer value in {group} metrics")
        if values != evidence[group]:
            raise ValueError(f"Retained values differ for {group} metrics")
        observed[group] = values

    metadata = observed["metadata"]
    if (
        metadata["intelligence_anchor_count"] + metadata["source_quality_anchor_count"]
        != metadata["metadata_records"]
    ):
        raise ValueError("Source metadata categories do not add up")
    return {
        "commit": evidence["commit"],
        "report_generated_at": report["generated_at"],
        "verified_git_blobs": len(blobs),
        **observed,
    }


if __name__ == "__main__":
    print(json.dumps(replay(), indent=2, sort_keys=True))
