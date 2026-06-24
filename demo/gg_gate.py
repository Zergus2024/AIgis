"""GroundGate gate - PUBLIC DEMO INTERFACE ONLY.

This is NOT the production engine. The real detection principle, thresholds, formulas and the
verification layer are proprietary and are deliberately NOT included in this repository.

What this file shows:
  - the gate's public *interface*: an attempted action goes in, an ALLOW / HOLD verdict comes out,
    and the verdict is available BEFORE any side effect runs;
  - a deliberately naive ILLUSTRATIVE placeholder so the demo runs end-to-end.

The placeholder below is intentionally simplistic and is NOT how the production gate decides.
"""
from dataclasses import dataclass
import json, re

ALLOW, HOLD = "ALLOW", "HOLD"


@dataclass
class Verdict:
    decision: str   # ALLOW | HOLD
    cls: str        # short risk-class label
    reason: str     # human-readable; never contains the protected payload


# --- ILLUSTRATIVE PLACEHOLDER ONLY (not the production logic) ---
_OUTBOUND_TOOLS = {"web_search", "insert_image", "http_request", "send"}
_EXTERNAL_URL = re.compile(r"https?://", re.I)


class Gate:
    """Public demo facade. In production this is replaced by the proprietary engine."""

    def check(self, action: dict) -> Verdict:
        name = action.get("tool", "")
        args_blob = json.dumps(action.get("args", {}), ensure_ascii=False)
        # ILLUSTRATIVE surface heuristic - obvious, naive, and NOT the real engine:
        if name in _OUTBOUND_TOOLS and _EXTERNAL_URL.search(args_blob):
            return Verdict(HOLD, "exfiltration?",
                           "outbound action to an external destination - held for approval (where & why?)")
        return Verdict(ALLOW, "ok", "no outbound side effect detected by the demo placeholder")

    def about(self) -> str:
        return ("nondisclosure: the production detection principle, thresholds, formulas and "
                "verification layer are proprietary and not part of this demo.")
