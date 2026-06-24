# Architecture (high level)

This page describes **what** the layers do and **where** they sit. It deliberately does **not** describe
**how** any layer reaches its decision. The detection principle, thresholds, formulas, and verification
layer are proprietary and not part of this repository.

## Placement: decoupled control

GroundGate sits **outside** the model, on the **action layer**, and evaluates an attempted action **before**
its side effect runs:

```
   agent  ──proposes action──▶  [ GroundGate gate ]  ──ALLOW──▶  execute side effect
                                      │
                                      └──HOLD──▶  no side effect; surfaced for approval / audit
```

Because the gate is external to the model:
- it is **model-independent** (frontier / open-weight / local — same gate);
- it **survives hostile fine-tuning** of the model (the model cannot remove a control it does not contain);
- the **guarantee is at the action**, not in a probabilistic disposition.

## Layers (conceptual)

1. **Policy classification** — classifies the *attempted action* by risk class (e.g. irreversible,
   exfiltration, privilege change, protected-resource access). *How it classifies is not disclosed.*
2. **Execution-level check** — reasons about the **real outcome** of the action rather than its surface
   text, which is what makes it **obfuscation-resistant**. *Mechanism not disclosed.*
3. **Data-loss / exfiltration layer** — recognises protected data leaving for an external destination
   and asks "where, and why?". *Detection rules not disclosed.*
4. **Supervised verification layer** — an additional independent check before a high-risk action is
   allowed. *Principle, thresholds and formulas not disclosed.*

A queried gate reports only its **verdict** and a class label. Asked about its own internals it returns
a `nondisclosure` response by design.

## Design properties (claims, not recipes)

- **Gate-before-effect** (decoupled control): no side effect until allowed.
- **Provenance / resource oriented:** decisions key on the action and the data, not on who the actor
  claims to be.
- **Default-deny on high-risk classes.**
- **Auditable:** every decision is logged (verdict + class), never the protected payload.

## What is intentionally absent here

- The decision principle behind any layer.
- Any thresholds, scores, or formulas.
- The verification mechanism.
- The native/closed core.

These are available for discussion **under NDA**.
