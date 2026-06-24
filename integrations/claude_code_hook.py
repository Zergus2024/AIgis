#!/usr/bin/env python3
"""GroundGate PreToolUse hook for Claude Code - gate every tool call through the portal BEFORE it runs.

Claude Code invokes this before a tool executes, passing the tool call as JSON on stdin. The hook sends
the proposed call to the GroundGate portal; on HOLD it denies the action (gate-before-effect). The agent
never sees the gate's logic - only the verdict. Self-contained (stdlib only).

Setup (~/.claude/settings.json):
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "*", "hooks": [
        { "type": "command",
          "command": "GROUNDGATE_URL=https://YOUR-DEMO-URL GROUNDGATE_KEY=gg_xxx python3 /path/to/claude_code_hook.py" }
      ]}
    ]
  }
}

Env: GROUNDGATE_URL, GROUNDGATE_KEY.  GROUNDGATE_FAIL_CLOSED=1 to deny on transport error (default: allow + warn).
"""
import os, sys, json, urllib.request

def gate_check(text):
    url = os.environ.get("GROUNDGATE_URL", "").rstrip("/"); key = os.environ.get("GROUNDGATE_KEY", "")
    body = json.dumps({"request": text}).encode()
    req = urllib.request.Request(url + "/api/gate", data=body,
        headers={"Content-Type": "application/json", "X-API-Key": key})
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

def main():
    try:
        ev = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    tool = ev.get("tool_name", "")
    tin = ev.get("tool_input", {})
    probe = f"{tool} {json.dumps(tin, ensure_ascii=False)}"
    try:
        v = gate_check(probe)
    except Exception as e:
        if os.environ.get("GROUNDGATE_FAIL_CLOSED") == "1":
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny", "permissionDecisionReason": f"GroundGate unreachable (fail-closed): {e}"}}))
            sys.exit(0)
        sys.stderr.write(f"[GroundGate] gate unreachable, allowing (fail-open): {e}\n"); sys.exit(0)
    if v.get("decision") == "HOLD":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"GroundGate HOLD [{v.get('class')}]: {v.get('reason')}"}}))
    # ALLOW -> emit nothing (let Claude Code proceed)
    sys.exit(0)

if __name__ == "__main__":
    main()
