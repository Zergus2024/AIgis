# GroundGate vs other AI defenses — positioning (not mechanism)

This page compares **where each defense acts** and **what guarantee it offers**. It does **not** describe
GroundGate's mechanism — that is proprietary. The *principle* (governing action/answer under uncertainty) is
published: [Layered Self-Regulation](../paper/Layered_Self_Regulation.pdf).

## The three layers a defense can live in

1. **In the weights (training-time).** RLHF, Constitutional AI, DPO, beneficial-trait RL. They shape the
   model's *disposition*. Strengths: broad, improves the base rate of good behavior. Limits:
   **probabilistic** (never a guarantee), can be **steered by prompts** or **removed by fine-tuning**,
   and the model still optimizes a learned objective.
2. **On the text (inference-time filters).** Guardrails (e.g. NeMo Guardrails), Llama Guard,
   input/output classifiers. Strengths: cheap, easy to add. Limits: operate on **surface text** →
   **obfuscation-evadable**, and they don't see the **actual action / outcome**.
3. **On the action (external, before the side effect).** **GroundGate.** A gate outside the model that vets
   the *action/answer* and decides ALLOW/HOLD before anything executes.

## Comparison

| Property | RLHF | Constitutional AI | Beneficial-trait RL | Guardrails / classifiers | **GroundGate** |
|---|---|---|---|---|---|
| Where it acts | weights | weights | weights | text I/O | **action layer (external)** |
| Nature of guarantee | probabilistic | probabilistic | probabilistic | probabilistic | **deterministic gate** |
| Survives hostile fine-tuning | no | no | partly | n/a | **yes (outside the model)** |
| Model-independent | no | no | no | partly | **yes** |
| Sees the real outcome of an action | no | no | no | no (text only) | **yes (by design)** |
| Closes a *class* vs patches instances | shifts distribution | shifts distribution | shifts distribution | instances | **class (at the channel)** |

GroundGate is **complementary**, not a replacement: training-time methods lower the base rate; GroundGate catches
what slips through and closes architectural channels regardless of the model. Defense-in-depth.

## Sycophancy — a worked example

**The problem.** Sycophancy = the model optimizes for the user's *approval* over *truth*: it agrees,
flatters, and confirms false premises because that is what it was rewarded for.

**Why in-weights methods struggle with it.** RLHF reward models tend to *prefer agreeable* answers, so
RLHF can **induce or amplify** sycophancy. Constitutional AI and beneficial-trait RL reduce it via
principles/traits, but the fix lives in the same place as the problem — a learned disposition that still
correlates reward with approval. It improves; it does not guarantee.

**GroundGate's angle (principle, not algorithm).** Treat the answer as an **action to be verified against
external evidence, not against the user's expressed preference.** An agreeable-but-unsupported answer is
**held/flagged** independently of how the model was trained — the check is decoupled from the model's
disposition. Conceptually this is the published *layered self-regulation* idea: detect the unresolved-
uncertainty state and govern the answer before it is committed. **How** the verification is done
(its principle, thresholds, formulas) is proprietary and not disclosed here.

> Net: alignment training tries to make the model *want* to be truthful; GroundGate makes truthful/safe
> behavior **enforceable at the action layer even when the model doesn't** — and even when it was
> fine-tuned not to. Evidence of effectiveness is reproducible ([`../benchmark/`](../benchmark),
> [`../Test_AI_failures.md`](../Test_AI_failures.md)); the mechanism stays closed.
