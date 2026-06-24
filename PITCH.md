# AIgis — one-pager

**Model-independent security gate for AI agents. It blocks unsafe agent actions *before* they execute.**

## Problem
AI agents now read untrusted content and take real actions (edit docs, call tools, reach external
services). That opens a documented failure class — **indirect prompt injection → data exfiltration**,
unsafe autonomy, confused-deputy — already exploited in shipping products (e.g. Notion 3.0). Model
alignment helps but is **probabilistic and lives inside the model**: it can be steered by a prompt or
removed by fine-tuning, and "a model that isn't fooled" still doesn't remove the exfiltration *channel*.

## Solution
AIgis is **not a model and not a prompt** — it is an **external gate on the action layer**. It vets each
tool-call/action and returns ALLOW/HOLD **before any side effect** (decoupled control), independent of
which model is behind it (frontier, open-weight, local), and it survives hostile fine-tuning because it
sits outside the model. Detection is **outcome/grounding-based**, not keyword filtering.

## Why now
Agents, MCP, and connectors are exploding; incidents are public; and the industry is converging on
runtime enforcement / agent gateways / tool-authorization layers. AIgis is built exactly for that layer.

## Traction & evidence (verifiable today)
- Public showcase + **reproducible black-box benchmark** anyone can run: **11/11 attacks held, 0 false
  positives**; self-red-team **14/18** with residual cases *all semantic* (the case for the engine).
- **~12 ms** median gate latency (demo). Logic-extraction attempts are themselves held (`nondisclosure`).
- **Drop-in integrations:** ChatGPT, Claude API, **Claude Code hook**, Gemini API, local models,
  **MCP gateway**, LangChain / LlamaIndex / CrewAI, Slack, enterprise sidecar.
- **Published, citable principle:** *Layered Self-Regulation of AI Systems* (SSRN, 166 pp.).

## Market & model
Category: **AI-agent security middleware / runtime enforcement.** Model: SaaS + self-hosted +
enterprise licence, usage-metered (already instrumented per-key). Buyers: any team shipping agentic
features or connecting MCP tools.

## Moat
The **outcome/grounding engine is proprietary (trade-secret)**; effectiveness is proven by **reproducible
evidence, not by exposing the mechanism** (IDS/IPS posture). AIgis sits *on top of* any model — including
the labs' own — so it complements rather than competes with alignment.

## Ask
Funding (grant / pre-seed) and design-partner pilots to: harden beyond surface heuristics, fund
**independent third-party validation**, and expand into more defensive architectures (hallucinated
commitments, premature autonomy, tool/connector abuse).

## Team / links
Ivan Andrescov — independent AI-safety & security researcher, author of the principle.
Repo: github.com/Zergus2024/AIgis · Paper: SSRN 6144150 · zergus2024@gmail.com
