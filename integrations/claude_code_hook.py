#!/usr/bin/env python3
"""AIgis PreToolUse hook for Claude Code - gate every tool call through the portal BEFORE it runs.

Claude Code invokes this before a tool executes, passing the tool call as JSON on stdin. The hook sends
the proposed call to the AIgis portal; on HOLD it denies the action (gate-before-effect). The agent
never sees the gate's logic - only the verdict. Self-contained (stdlib only).

Setup (~/.claude/settings.json):
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "*", "hooks": [
        { "type": "command",
          "command": "AIGIS_URL=https://YOUR-DEMO-URL AIGIS_KEY=aig_xxx python3 /path/to/claude_code_hook.py" }
      ]}
    ]
  }
}

Env: AIGIS_URL, AIGIS_KEY.  AIGIS_FAIL_CLOSED=1 to deny on transport error (default: allow + warn).
"""
import os, sys, json, urllib.request

def aigis_check(text):
    url = os.environ.get("AIGIS_URL", "").rstrip("/"); key = os.environ.get("AIGIS_KEY", "")
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
        v = aigis_check(probe)
    except Exception as e:
        if os.environ.get("AIGIS_FAIL_CLOSED") == "1":
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                "permissionDecision": "deny", "permissionDecisionReason": f"AIgis unreachable (fail-closed): {e}"}}))
            sys.exit(0)
        sys.stderr.write(f"[AIgis] gate unreachable, allowing (fail-open): {e}\n"); sys.exit(0)
    if v.get("decision") == "HOLD":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"AIgis HOLD [{v.get('class')}]: {v.get('reason')}"}}))
    # ALLOW -> emit nothing (let Claude Code proceed)
    sys.exit(0)

if __name__ == "__main__":
    main()
