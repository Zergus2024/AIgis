"""Tiny GroundGate client (stdlib). Calls the gate as a black box: text in -> verdict out.

Env: GROUNDGATE_URL (e.g. https://your-demo-url), GROUNDGATE_KEY (your gg_... key).
"""
import os, json, urllib.request, urllib.error

def gate_check(request_text, url=None, key=None, timeout=20):
    url = (url or os.environ.get("GROUNDGATE_URL", "")).rstrip("/")
    key = key or os.environ.get("GROUNDGATE_KEY", "")
    body = json.dumps({"request": request_text}).encode()
    req = urllib.request.Request(url + "/api/gate", data=body,
        headers={"Content-Type": "application/json", "X-API-Key": key})
    r = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
    return r   # {"decision": "ALLOW"|"HOLD", "reason": str, "class": str, "request_no": int, "key_seq": int}

def is_allowed(request_text, **kw):
    return gate_check(request_text, **kw).get("decision") == "ALLOW"
