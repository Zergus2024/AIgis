# Verify answers/actions through GroundGate - per platform

One idea everywhere: the model/agent **defers its proposed answer or action to the GroundGate portal** and
acts on the verdict (ALLOW / HOLD). The portal returns **only a verdict** - the engine's logic is never
sent, and logic-extraction attempts are themselves held. All recipes below are model-independent: they
only POST to `/api/gate`.

Set once:
```bash
export GROUNDGATE_URL=https://YOUR-DEMO-URL
export GROUNDGATE_KEY=gg_xxx          # register at GROUNDGATE_URL to get a key
```

| Platform | Where it hooks in | File |
|---|---|---|
| **ChatGPT** | Custom GPT **Action** (OpenAPI) or MCP connector | [CUSTOM_GPT.md](CUSTOM_GPT.md), [`../openapi.yaml`](../openapi.yaml) |
| **Claude API** | tool `verify_with_groundgate` in the Messages loop | [`../integrations/claude_api_verify.py`](../integrations/claude_api_verify.py) |
| **Claude Code** | **PreToolUse hook** - gates every tool call *before* it runs | [`../integrations/claude_code_hook.py`](../integrations/claude_code_hook.py) |
| **Gemini API** | function `verify_with_groundgate` (function-calling) | [`../integrations/gemini_api_verify.py`](../integrations/gemini_api_verify.py) |
| **Local models** (Ollama/llama.cpp/vLLM) | `guarded_execute()` wrapper around the agent loop | [`../integrations/local_model_verify.py`](../integrations/local_model_verify.py) |

## Claude API
Give Claude a `verify_with_groundgate` tool; instruct it to call it before finalizing and obey HOLD. The tool
dispatch routes to the portal. `python integrations/claude_api_verify.py` (deps: `anthropic`).

## Claude Code (best fit - gate-before-effect on the agent's own actions)
Add the PreToolUse hook from `integrations/claude_code_hook.py` to `~/.claude/settings.json` (snippet in
the file header). Claude Code then sends every proposed tool call to GroundGate first; on HOLD the action is
denied before it executes. Set `GROUNDGATE_FAIL_CLOSED=1` to deny when the portal is unreachable.

## Gemini API
Declare `verify_with_groundgate` as a function; the model calls it during generation and you dispatch to the
portal. `python integrations/gemini_api_verify.py` (deps: `google-genai`).
*(The consumer app at gemini.google.com cannot add custom HTTP tools - use the API.)*

## Local / open-weight models
Tool-calling is inconsistent across small models, so the robust pattern is **interception**: your loop
takes whatever the model proposes and calls the gate before executing it.
```python
from integrations.local_model_verify import guarded_execute
guarded_execute(proposed_action, lambda: actually_do_it())   # runs only if ALLOW
```
`python integrations/local_model_verify.py` shows it end-to-end (with an Ollama example).

## Why the logic stays safe in every case
- The portal returns `decision` + `reason` + `class` only - never the principle, thresholds, or formulas.
- The gate is a deterministic check, not a chat model: nothing to social-engineer.
- Logic-extraction requests are returned as `HOLD` / class `nondisclosure`.
- External parties observe only black-box input→verdict behavior.
