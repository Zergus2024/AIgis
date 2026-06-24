# Integrating GroundGate into agent frameworks & enterprise stacks

GroundGate governs **actions**, and every agent framework funnels actions through a tool callable, a tool
call, or an outbound request. You insert GroundGate at that point: vet the call, run it only on ALLOW. One
reusable helper — [`../integrations/frameworks_guard.py`](../integrations/frameworks_guard.py) — covers
the Python-callable cases; the rest are gateway/proxy patterns.

```bash
export GROUNDGATE_URL=https://YOUR-DEMO-URL
export GROUNDGATE_KEY=gg_xxx
```

## Agent frameworks (wrap the tool callable)
All of these end at a Python function — decorate it with `@guard_tool`:

```python
from integrations.frameworks_guard import guard_tool

@guard_tool(name="send_email")
def send_email(to, body): ...
```

| Framework | Where to apply | Note |
|---|---|---|
| **LangChain** | wrap each `Tool`/`@tool` function with `@guard_tool`; or add an `on_tool_start` callback that calls `gate_check` and raises to block | gates tool execution inside `AgentExecutor` |
| **LlamaIndex** | wrap the function passed to `FunctionTool.from_defaults(fn=...)` | gates the agent's tool use |
| **CrewAI** | wrap the `@tool` callable each agent uses | gates per-agent actions |
| **Plain function-calling** (OpenAI/Anthropic/Gemini) | wrap your dispatch handlers; or see [INTEGRATIONS.md](INTEGRATIONS.md) for the explicit `verify_with_groundgate` tool | model-independent |

## MCP (Model Context Protocol)
Run GroundGate as an **MCP gateway** in front of any MCP server (Notion, GitHub, filesystem, …): it inspects
each tool-call and forwards only ALLOWED ones. Pattern + demo: [`../notion/`](../notion). This directly
satisfies "only add MCP servers you trust" — GroundGate becomes the trust layer for all MCP traffic.

## Notion / Slack (and similar SaaS agents)
The agent acts on these via tool calls / their APIs / MCP. Gate those calls:
- **Notion:** GroundGate MCP gateway in front of the Notion MCP server (see `notion/`), or wrap the API client.
- **Slack:** wrap the bot's outbound actions (post message, upload file, call external webhook) with
  `@guard_tool`, or gate at the app's action dispatcher. Stops a prompt-injected bot from exfiltrating
  channel data to an external destination.

## Enterprise deployment
- **Sidecar / reverse proxy:** place GroundGate in front of the agent's tool/egress traffic; deny on HOLD.
- **API gateway plugin:** call `/api/gate` from the gateway before forwarding agent-originated calls.
- **Fail-closed** in production (`GROUNDGATE_FAIL_CLOSED=1` in the Claude Code hook; `fail_closed=True` in
  `guard_tool`) so an unreachable gate blocks rather than allows.
- **Audit:** every decision is logged (verdict + class, never the payload) - forward to your SIEM.
- **Self-hosted** option keeps all traffic in your perimeter; the engine stays a black box either way.

## Why this is safe to integrate
Every integration only **POSTs to `/api/gate`** and reads a verdict. No gate logic ships with the
integration; logic-extraction attempts return `nondisclosure`. You can self-host the gate and still
treat it as a black box.
