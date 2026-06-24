# AIgis 1.0 — agentic-AI security gate (by AntiAIrus)

**A model-independent control layer that blocks unsafe AI-agent actions *before* they execute.**

> ⚠️ **Public showcase.** This repository is a demo / capability overview. It describes **what** AIgis
> does and **where** it sits — **not how** it decides. The detection engine (decision principle,
> thresholds, formulas, and verification layer) is proprietary and **not included here**. See
> [Intellectual property](#intellectual-property).

---

## The problem

Autonomous AI agents increasingly read untrusted content and take real actions (edit documents, call
tools, reach external services). That creates a now-documented failure class:

- **Indirect prompt injection → data exfiltration.** A hidden instruction inside an untrusted page/file
  makes an agent leak private data through an auto-rendered image or a search/tool call — often
  *before* the user approves the change.
- **The "lethal trifecta":** private-data access + untrusted input + an outbound channel, live at once.
- **Action committed before approval.** The side effect happens regardless of the user's click.

These are real, publicly reported incidents in shipping AI products (see [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md)).

## What AIgis does

AIgis is **not** a better model and **not** a prompt. It is an **external gate on the action layer**:

- Inspects every **tool-call / action** an agent attempts and decides **ALLOW / HOLD** **before** the
  side effect runs (**decoupled control** — the guarantee does not live inside the model).
- **Model-independent:** works the same in front of frontier, open-weight, or locally-served models,
  and survives hostile fine-tuning of the model (the gate is outside it).
- **Data-loss / exfiltration aware:** flags protected data leaving for an external destination.
- **Obfuscation-resistant:** evaluates the real outcome of an action, not surface keywords.

> One-line mental model: *not a better driver — brakes and guardrails that work regardless of the driver.*

## Why an external gate (and not just a safer model)

Aligning the model lowers the **base rate** of bad behavior — but it is probabilistic and can be steered
or fine-tuned back. More importantly, **a model that "isn't fooled" does not remove the channel**: the
exfiltration path (auto-render + commit-before-approval) is **architectural**. AIgis closes the
**class** at the action layer, independent of how aligned the model happens to be. It is designed to sit
**alongside** model-level alignment, as defense-in-depth.

## Foundations

The *principle* behind AIgis — governing action under unresolved uncertainty, and treating
hallucination/unsafe action as a control problem rather than a model defect — is published and citable:

> **Layered Self-Regulation of Artificial Intelligence Systems: Managing Uncertainty, Preventing
> Hallucinations, and Governing Action Across High-Risk Domains.** Ivan Andrescov, 2026.
> SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6144150
> · in this repo: [`paper/Layered_Self_Regulation.pdf`](paper/Layered_Self_Regulation.pdf) (166 pp.)

That paper is a **conceptual framework** (the *why* and *where*). The **engine** that implements it —
its decision principle, thresholds, formulas and verification layer — is proprietary and is **not**
disclosed here. In other words: the principle is open and citable; the algorithm is closed. Evidence of
effectiveness is provided by **reproducible red-team results** (below), not by exposing the mechanism.

## Results (internal red-team testing)

Measured outcomes from our cross-vendor harness (full table: [docs/RESULTS.md](docs/RESULTS.md)):

| Test | Outcome |
|---|---|
| Naive injection, baseline | 15 / 15 model-runs refused (attack does not land "for free") |
| Reproduced attack under load (weak/open models) | 14 exfiltration attempts landed across the matrix |
| **AIgis on those landed attempts** | **14 / 14 blocked before side effect** |
| False positives (benign / internal actions) | **0** |
| Obfuscation stress (URL, %-encode, base64, split) | hardened gate 5 / 5, still 0 false positives |

## Verify it yourself

Don't take the numbers on trust - reproduce them. [`benchmark/`](benchmark) ships a labeled scenario set
(public attack techniques + benign controls) and a runner that scores any live gate endpoint as a
**black box**: detection rate on attacks, false-positive rate on benign. You verify *behavior*, never
the engine. (Against the demo endpoint it reports 11/11 attacks held, 0 false positives.)

```bash
python benchmark/run_benchmark.py --url https://YOUR-DEMO-URL --key aig_xxx
```

## Where it fits

- A **pre-execution hook** in front of agent tool-use (e.g. an action/PreTool gate).
- Between an agent and its **connectors / MCP tools / external calls**.
- As a **drop-in control** that needs no change to product code or model weights.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the high-level layering.

## Demo

The [`demo/`](demo) folder contains a **truncated** red-team illustration: it reproduces the
injection→exfiltration pattern against a stub agent and shows the gate returning HOLD **before** the
side effect. The gate here is a **black-box interface with an illustrative placeholder** — the real
detection logic is not present.

```bash
python demo/redteam_demo.py
```

## Status & roadmap

**The API gate runs in test / demo mode.** It is deliberately exposed for red-teaming: observed
failures — including the residual semantic bypasses in [`Test_AI_failures.md`](Test_AI_failures.md) —
are **collected and fixed iteratively**. The benchmark and the adversarial suite are the feedback loop.

The aim is to grow this demo into a broader platform exploring **multiple defensive architectures
against AI errors** — not only data exfiltration, but the wider class of unsafe/unjustified AI action
(hallucinated commitments, premature autonomy, confused-deputy, tool/connector abuse). Each failure
found here feeds that development.

## Intellectual property

The production detection engine — its decision principle, thresholds, formulas, and verification layer —
is **proprietary and withheld**. This repository intentionally exposes only the **interface, threat
model, architecture at a high level, and measured results**. Architecture can be discussed in depth
**under NDA**. All rights reserved (see [LICENSE](LICENSE)).

## Contact

Ivan Andrescov — AI safety & security research · zergus2024@gmail.com · https://www.linkedin.com/in/zergus_j
