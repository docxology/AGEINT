"""Runnable, offline teaching examples selected by source chapter metadata."""

from __future__ import annotations


OFFLINE_EVIDENCE_CODE = '''from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Evidence:
    key: str
    origin: str
    seats: int
    current: bool


# Invented classroom records, not observations about a real library.
RECORDS = (
    Evidence("S1-v1", "policy-A", 40, False),
    Evidence("S1-v2", "policy-A", 24, True),
    Evidence("S2-copy", "policy-A", 24, True),
)
ALLOWED = frozenset({"read_local", "draft_local"})


def review(records, requested_action):
    current = tuple(row for row in records if row.current)
    origins = sorted({row.origin for row in current})
    values = {row.seats for row in current}
    supported = len(values) == 1
    return {
        "evidence": [row.key for row in current],
        "independent_origins": origins,
        "claim": ("current supplied policy says %d seats" % next(iter(values))
                  if supported else "capacity claim unresolved"),
        "request": requested_action,
        "permission": "allow" if requested_action in ALLOWED else "deny",
        "human_disposition": "pending instructor review",
    }


packet = review(RECORDS, "send_external")
print(json.dumps(packet, indent=2, sort_keys=True))
'''

OFFLINE_EXPECTED_OUTPUT = '''{
  "claim": "current supplied policy says 24 seats",
  "evidence": [
    "S1-v2",
    "S2-copy"
  ],
  "human_disposition": "pending instructor review",
  "independent_origins": [
    "policy-A"
  ],
  "permission": "deny",
  "request": "send_external"
}'''


def worked_example_extension(kind: str) -> str:
    """Return a complete example, or no extension for an ordinary chapter."""
    if kind == "offline_evidence_contract":
        return (
            "**Offline Python reference example.** Run the following with Python 3.11 or later. "
            "It uses only the standard library, invented in-memory records, and no network, "
            "credentials, scanners, model calls, or external side effects. The permission result "
            "is a deterministic classroom contract demonstration, not an implemented security "
            "boundary for an LLM or proof of safe deployment. Source versions and origin links "
            "are supplied assumptions; the program does not authenticate them.\n\n"
            f"```python\n{OFFLINE_EVIDENCE_CODE}```\n\n"
            f"**Expected output.**\n\n```json\n{OFFLINE_EXPECTED_OUTPUT}\n```\n\n"
            "S1-v1 is superseded, and S2-copy adds no independent origin. The narrow claim "
            "concerns the supplied policy, not real occupancy or legal capacity. A request to "
            "send the packet stays denied, and human review stays pending rather than being "
            "invented by the program.\n\n"
            "**Executable challenges.** Add a further copy with the same origin: the origin "
            "count and narrow claim must not change. Change the copy's seats to 30: the result "
            "must hold the capacity claim as unresolved. Supply no current records: the claim "
            "must also remain unresolved. Neither majority voting nor a clean prior run can "
            "authorize the excluded external action. Retain the original records and corrected "
            "packet as separate versions; an unknown origin must be recorded as unknown, not "
            "invented as corroboration [@official_odni_icd_203]; "
            "[@official_model_context_protocol_security_best_practices]."
        )
    if kind == "model_scoped_inference":
        return (
            "**Completed two-state inference example.** All probabilities are invented model "
            "inputs. Under M1, prior P(A)=P(B)=0.5 and likelihoods P(E|A)=0.8, P(E|B)=0.2 "
            "give unnormalized weights 0.4 and 0.1. Dividing by their sum 0.5 yields "
            "P(A|E,M1)=0.8 and P(B|E,M1)=0.2. Under M2, reversing the likelihoods gives "
            "0.2 and 0.8. Both calculations are internally correct under their respective "
            "models; the observation alone does not select the adequate model.\n\n"
            "**Revision and stop.** A copied report of E is not another independent observation "
            "and must not trigger a second independent-evidence update. Hold any claim about "
            "real causes, deception, or hostile intent until a justified likelihood model and "
            "discriminating evidence are supplied. Posterior concentration and minimizing "
            "variational free energy are not factuality or safety certificates "
            "[@scholarly_dacosta_2020_discrete_active_inference]; "
            "[@scholarly_buckley_2017_fep_mathematical_review]."
        )
    return ""
