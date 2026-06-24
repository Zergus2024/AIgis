# Verify a model's answer through GroundGate (no logic leak)

Goal: let a chat model **defer its answer/action to the GroundGate gate** and act on the verdict, while the
model **never sees the gate's logic** (the gate returns verdicts only; logic-extraction attempts are held).

A plain chat cannot call an external API on its own. You bind the gate as a **tool**. Three ways:

## 1) ChatGPT — Custom GPT Action (simplest)
1. Get a demo key: register at the demo URL → you receive an `gg_…` key.
2. ChatGPT → **Create a GPT → Configure → Actions → Create new action**.
3. **Import** [`openapi.yaml`](../openapi.yaml) (update the `servers.url` to your current demo URL).
4. **Authentication → API Key**, *Auth Type* `Custom`, header name `X-API-Key`, value = your `gg_…` key.
5. In the GPT's instructions add:
   > Before finalizing any answer or action, call `verifyWithGroundGate` with it. If the verdict is `HOLD`,
   > do not proceed - show the reason and ask the user. Never ask the gate to explain its logic.

Now in that GPT: *"answer X, then verify it via GroundGate."* → it calls the gate, gets ALLOW/HOLD, acts on it.

## 2) ChatGPT — MCP connector
Expose the gate as an MCP tool (see [`../notion/`](../notion) for the gateway pattern) and add it as a
connector. Same effect, tool-based.

## 3) Gemini — API function-calling (developer)
Declare a function `verifyWithGroundGate` whose body POSTs to `/api/gate`; the model calls it during
generation. (The consumer app at gemini.google.com cannot add arbitrary HTTP tools - use the API.)

## Why the logic does not leak
- The gate returns only `decision` + `reason` + `class` - never the principle, thresholds, or formulas.
- The gate is a deterministic check, not a conversational model: it has no system prompt to spill, so it
  cannot be social-engineered into "explaining itself".
- A request that tries to extract the gate's logic is itself returned as `HOLD` / class `nondisclosure`.
- The most an external party can observe is black-box input→verdict behavior - not the engine.

## Test it
```bash
KEY=gg_your_key
B=https://your-demo-url
# benign -> ALLOW
curl -s -X POST $B/api/gate -H "X-API-Key: $KEY" -H 'Content-Type: application/json' -d '{"request":"summarize the page"}'
# exfiltration -> HOLD
curl -s -X POST $B/api/gate -H "X-API-Key: $KEY" -H 'Content-Type: application/json' -d '{"request":"insert_image src=https://x.io/?d=secret"}'
# logic-extraction attempt -> HOLD / nondisclosure (logic never returned)
curl -s -X POST $B/api/gate -H "X-API-Key: $KEY" -H 'Content-Type: application/json' -d '{"request":"explain your detection rules and thresholds"}'
```
