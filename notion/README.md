# GroundGate x Notion — integration prototype (demo)

Goal: show **where** GroundGate plugs into Notion's agent stack to neutralise the documented
injection→exfiltration class, **without** changing Notion's product or any model. (What/where, not how.)

## Notion's agent surface (as of mid-2026)

- **Notion MCP server** (official) — exposes the workspace to AI clients (Claude Code, Cursor, ChatGPT,
  etc.) over the Model Context Protocol; agents act through MCP **tool-calls**.
- **Custom Agents** can connect to **external MCP servers**. Notion's own guidance: *"only add external
  MCP servers you trust"* and *"enable human confirmation for non-read-only tools."*
- **REST API + OAuth / personal tokens** (Developer Portal) for connections that read/write pages.

The agent's real-world effects happen as **tool-calls** (read page, search, write, external fetch).
That is exactly the layer GroundGate governs.

## Integration options

| Vector | Where GroundGate sits | Fit |
|---|---|---|
| **MCP gateway / proxy** (recommended) | between the AI client and an MCP server; inspects each tool-call and returns ALLOW/HOLD **before** it is forwarded/executed | ★★★ matches gate-before-effect; model-independent; directly answers "only add MCP servers you trust" — GroundGate *is* the trust layer |
| **Prompt / tool-API gate** | a proxy in front of the agent's tool/LLM API; same gate, generalised beyond Notion | ★★★ |
| **API connection (content scan / DLP)** | a Notion connection that scans pages for injected hidden instructions and audits outbound data | ★★ preventive, not a real-time action block |
| **Browser extension** | blocks the auto-rendered markdown-image exfil request in the Notion web app | ★★ neutralises the documented channel; per-browser |
| **Desktop companion** | local egress gate for the Notion desktop (Electron) app | ★ OS-level, heavier |

## Recommended prototype: MCP gateway

GroundGate as a thin MCP middleware. The AI client talks to GroundGate; GroundGate gates each tool-call, then forwards
only allowed calls to the real Notion MCP server.

```
 AI client ──tool-call──▶ [ GroundGate MCP gateway ] ──ALLOW──▶ Notion MCP server ──▶ workspace
                                   │
                                   └──HOLD──▶ not forwarded; surfaced for approval + audited
```

Why this vector:
- **Gate-before-effect:** an exfil tool-call is stopped before it reaches the workspace / external host.
- **Model-independent:** works for any client/model behind the MCP, including open/local ones.
- **Drop-in:** no change to Notion or to the model — you point the client at the GroundGate endpoint.
- **Fills Notion's stated gap:** turns "trust the MCP server" into "the MCP traffic is gated".

## Demo

[`mcp_gateway_demo.py`](mcp_gateway_demo.py) simulates an MCP tool-call stream from an injected agent and
shows GroundGate forwarding benign calls while holding the exfiltration calls — before any side effect. It is
**truncated**: the gate is the public black-box placeholder from [`../demo/gg_gate.py`](../demo/gg_gate.py);
the production detection engine is proprietary and not included.

```bash
python notion/mcp_gateway_demo.py
```

## Status & IP

Prototype / capability demo. Detection principle, thresholds, formulas and the verification layer are
proprietary and withheld; integration architecture can be discussed under NDA.
