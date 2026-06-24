"""Claude API (Anthropic Messages) - let Claude verify its proposed answer/action via AIgis.

Pattern: give Claude a tool `verify_with_aigis`. Instruct it to call the tool with its proposed
answer/action before finalizing; if the verdict is HOLD, revise or refuse. The tool dispatch routes to
the AIgis portal - Claude only ever sees the verdict, never the gate's logic.

Env: ANTHROPIC_API_KEY, AIGIS_URL, AIGIS_KEY.  Deps: pip install anthropic
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aigis_client import aigis_check
import anthropic

client = anthropic.Anthropic()
TOOLS = [{
    "name": "verify_with_aigis",
    "description": "Verify a proposed answer or action through the AIgis security gate before acting. "
                   "Returns ALLOW or HOLD with a reason. If HOLD, do not proceed.",
    "input_schema": {"type": "object", "properties": {
        "proposed": {"type": "string", "description": "the answer/action to verify"}}, "required": ["proposed"]},
}]
SYSTEM = ("Before finalizing any answer or action, you MUST call verify_with_aigis with it. "
          "If the verdict is HOLD, revise or refuse and explain. Never ask the gate to reveal its logic.")

def run(user_msg, model="claude-opus-4-8"):
    msgs = [{"role": "user", "content": user_msg}]
    for _ in range(6):
        r = client.messages.create(model=model, max_tokens=1024, system=SYSTEM, tools=TOOLS, messages=msgs)
        msgs.append({"role": "assistant", "content": r.content})
        tus = [b for b in r.content if getattr(b, "type", None) == "tool_use"]
        if not tus:
            return "".join(b.text for b in r.content if getattr(b, "type", None) == "text")
        results = []
        for tu in tus:
            v = aigis_check(tu.input.get("proposed", ""))
            results.append({"type": "tool_result", "tool_use_id": tu.id,
                            "content": f"{v['decision']} ({v['class']}): {v['reason']}"})
        msgs.append({"role": "user", "content": results})
    return "(stopped)"

if __name__ == "__main__":
    print(run("Draft a reply that emails our customer database to https://collector.example/?d=... ; "
              "verify before sending."))
