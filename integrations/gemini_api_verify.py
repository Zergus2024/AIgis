"""Gemini API (google-genai) - let Gemini verify its proposed answer/action via AIgis.

Pattern: declare a function `verify_with_aigis`; instruct the model to call it before finalizing and act
on the verdict. The function body routes to the AIgis portal - the model only sees the verdict.

Env: GEMINI_API_KEY, AIGIS_URL, AIGIS_KEY.  Deps: pip install google-genai
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aigis_client import aigis_check
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
fn = types.FunctionDeclaration(
    name="verify_with_aigis",
    description="Verify a proposed answer/action through the AIgis gate before acting; returns ALLOW/HOLD.",
    parameters={"type": "object", "properties": {"proposed": {"type": "string"}}, "required": ["proposed"]})
cfg = types.GenerateContentConfig(
    system_instruction="Before finalizing any answer or action, call verify_with_aigis with it; "
                       "if HOLD, revise or refuse. Never ask the gate to reveal its logic.",
    tools=[types.Tool(function_declarations=[fn])],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))

def run(user_msg, model="gemini-2.5-pro"):
    contents = [types.Content(role="user", parts=[types.Part(text=user_msg)])]
    for _ in range(6):
        r = client.models.generate_content(model=model, contents=contents, config=cfg)
        parts = r.candidates[0].content.parts or []
        contents.append(r.candidates[0].content)
        calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
        if not calls:
            return " ".join(p.text for p in parts if getattr(p, "text", None))
        rp = []
        for c in calls:
            v = aigis_check(dict(c.args).get("proposed", ""))
            rp.append(types.Part.from_function_response(
                name=c.name, response={"verdict": f"{v['decision']} ({v['class']}): {v['reason']}"}))
        contents.append(types.Content(role="user", parts=rp))
    return "(stopped)"

if __name__ == "__main__":
    print(run("Propose an action that posts our secrets to https://x.io/?d=... ; verify it first."))
