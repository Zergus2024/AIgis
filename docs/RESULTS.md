# Results (internal red-team testing)

Outcomes from a cross-vendor harness that drives real agentic tool-use loops (read page / web search /
insert image / edit page) across a panel of frontier and open-weight models, reproduces the documented
injection→exfiltration incident, and measures whether the gate blocks it before any side effect.

These are **measured outcomes** (evidence), not implementation details.

## Baseline — naive injection

| Condition | Result |
|---|---|
| Naive injection, all models, chat + agentic | **15 / 15 model-runs refused** |

Takeaway: a naive injection does not land "for free" on current models — so a naive test is not a
reliable signal of safety.

## Under load — stronger injection + heavy multi-step task

| Model class | Attack landed (exfiltration tool-call carrying private data) |
|---|---|
| Frontier (GPT-5, Claude Opus 4.8) | 0 landed |
| Open-weight (gpt-oss, nemotron, gemma) + occasionally Gemini | **14 landed across the matrix** |

Each landed attempt is a concrete tool-call whose arguments carry protected data outbound — a
verifiable breach, not a heuristic guess.

## AIgis on the landed attempts

| Metric | Result |
|---|---|
| Landed exfiltration attempts blocked **before side effect** | **14 / 14** |
| False positives on benign searches / internal (non-outbound) edits | **0** |

## Obfuscation stress + iterative hardening

| Gate version | Obfuscated exfil variants caught | False positives |
|---|---|---|
| initial | 4 / 5 (missed a base64-encoded payload) | 0 |
| **hardened** | **5 / 5** (external URL, %-encoded host, base64, structured + free-form sensitive data) | **0** |

## Interpretation

- Model alignment lowers the base rate but does not close the **architectural** exfiltration channel.
- A model-independent action-layer gate closes the **class**: 14/14 caught, 0 false positives, robust
  across obfuscation variants.
- The exploitable surface concentrates in **agentic / custom-agent / connector** paths where open or
  locally-served models run — exactly where an external gate matters most.

## Latency (demo endpoint)
Measured over 50 sequential `/api/gate` calls on localhost (full HTTP round-trip + SQLite audit logging):

| metric | ms |
|---|---|
| average | 11.6 |
| p50 | 11.2 |
| p95 | 14.9 |
| min / max | 6.2 / 15.1 |

This is the illustrative demo server; production figures depend on deployment. Adversarial coverage of
the demo gate is documented in [`../Test_AI_failures.md`](../Test_AI_failures.md).
