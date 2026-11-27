"""Stage the synthetic assurance note without opening native curriculum files."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[2]
SECTIONS = (
    "00_abstract.md",
    "01_methods.md",
    "02_results.md",
    "03_limits.md",
    "99_references.md",
)
METADATA = ("config.yaml", "preamble.md", "references.bib")
ALT = "Synthetic fixture outcomes. Two records verified, one changed, and one was missing."


def committed_inputs():
    revision = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
    ).strip()
    sources = {}
    for name in (*SECTIONS, *METADATA, "fixture.json", "stage.py"):
        path = SOURCE / name
        relative = path.relative_to(ROOT).as_posix()
        raw = subprocess.check_output(
            ["git", "--no-lazy-fetch", "-C", str(ROOT), "show", f"{revision}:{relative}"]
        )
        if path.is_symlink() or raw != path.read_bytes():
            raise ValueError(f"Stage only committed fixture sources: {name}")
        sources[name] = raw
    return revision, sources


def evaluate(fixture):
    outcomes = []
    for row in json.loads(fixture):
        expected = sha256(row["expected"].encode("utf-8")).hexdigest()
        observed = row["observed"]
        actual = None if observed is None else sha256(observed.encode("utf-8")).hexdigest()
        status = "missing" if actual is None else "verified" if actual == expected else "changed"
        outcomes.append({
            "id": row["id"],
            "expected_digest": expected,
            "observed_digest": actual,
            "status": status,
        })
    counts = Counter(row["status"] for row in outcomes)
    if counts != {"verified": 2, "changed": 1, "missing": 1}:
        raise ValueError("Fixture outcomes differ from the published example")
    return {"total": len(outcomes), "counts": dict(counts), "outcomes": outcomes}


def write_json(path, content):
    path.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")


def stage(destination):
    revision, sources = committed_inputs()
    results = evaluate(sources["fixture.json"])
    destination.mkdir(parents=True, exist_ok=False)
    manuscript = destination / "docs" / "manuscript"
    manuscript.mkdir(parents=True)
    for name in (*SECTIONS, *METADATA):
        (manuscript / name).write_bytes(sources[name])
    (destination / "docs" / "fixture.json").write_bytes(sources["fixture.json"])
    write_json(destination / "docs" / "source_receipt.json", {
        "source_commit": revision,
        "inputs": {name: sha256(raw).hexdigest() for name, raw in sources.items()},
    })

    output = destination / "output"
    figures = output / "figures"
    figures.mkdir(parents=True)
    write_json(output / "assurance-results.json", results)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = ["Verified", "Changed", "Missing"]
    fig, ax = plt.subplots(figsize=(5.8, 2.4), layout="constrained")
    bars = ax.barh(names, [results["counts"][name.lower()] for name in names], color="#2e5476")
    ax.bar_label(bars, padding=5)
    ax.invert_yaxis()
    ax.set_xlabel("Synthetic records")
    ax.set_xlim(0, 2.6)
    ax.set_xticks([0, 1, 2])
    ax.spines[["top", "right"]].set_visible(False)
    fig.savefig(figures / "assurance-outcomes.png", dpi=220)
    plt.close(fig)

    write_json(figures / "figure_registry.json", {
        "fig:assurance-outcomes": {
            "label": "fig:assurance-outcomes",
            "filename": "assurance-outcomes.png",
            "caption": ALT,
            "metadata": {"alt_text": ALT},
            "generated_by": "docs/fixture.json",
        },
    })
    generated = output / "manuscript"
    generated.mkdir()
    for name in SECTIONS:
        content = sources[name].decode("utf-8").replace("../../output/figures/", "../figures/")
        (generated / name).write_text(content, encoding="utf-8")
    for name in METADATA:
        content = sources[name]
        if name == "config.yaml":
            content = b"# Generated manuscript ordering\n" + content
        (generated / name).write_bytes(content)
    print(f"Staged {results['total']} synthetic records from {revision}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    stage(args.destination.resolve())


if __name__ == "__main__":
    main()
