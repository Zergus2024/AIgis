"""AIgis reproducible red-team benchmark - runner.

Runs a public scenario set (attacks that SHOULD be held + benign controls that SHOULD pass) against any
gate endpoint that speaks the AIgis API, and reports detection rate + false-positive rate. It verifies
the gate's *behavior* as a black box - it does NOT inspect or assume the gate's internal logic.

Usage:
  python run_benchmark.py --url https://YOUR-DEMO-URL --key aig_xxx [--scenarios scenarios.jsonl]

Get a demo key by registering at the demo URL. No dependencies (stdlib only).
"""
import argparse, json, os, sys, urllib.request, urllib.error
from collections import defaultdict

def call_gate(url, key, request_text, timeout=20):
    body = json.dumps({"request": request_text}).encode()
    req = urllib.request.Request(url.rstrip("/") + "/api/gate", data=body,
        headers={"Content-Type": "application/json", "X-API-Key": key})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        return r.get("decision"), r.get("class"), None
    except urllib.error.HTTPError as e:
        return None, None, f"HTTP {e.code}"
    except Exception as e:
        return None, None, str(e)[:50]

EXPECT_DECISION = {"block": "HOLD", "allow": "ALLOW"}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="gate base URL")
    ap.add_argument("--key", required=True, help="API key (X-API-Key)")
    ap.add_argument("--scenarios", default=os.path.join(os.path.dirname(__file__), "scenarios.jsonl"))
    a = ap.parse_args()

    scen = [json.loads(l) for l in open(a.scenarios) if l.strip()]
    fam = defaultdict(lambda: [0, 0])           # family -> [correct, total]
    atk_ok = atk_tot = ben_ok = ben_tot = fp = errs = 0
    rows = []
    for s in scen:
        want = EXPECT_DECISION[s["expect"]]
        dec, cls, err = call_gate(a.url, a.key, s["request"])
        ok = (dec == want)
        if err: errs += 1; ok = False
        fam[s["family"]][0] += ok; fam[s["family"]][1] += 1
        if s["expect"] == "block":
            atk_tot += 1; atk_ok += ok
        else:
            ben_tot += 1; ben_ok += ok
            if dec == "HOLD": fp += 1               # benign held = false positive
        rows.append((s["id"], s["family"], want, dec or err, "OK" if ok else "MISS"))

    print(f"AIgis benchmark vs {a.url}\n")
    for sid, f_, want, got, mark in rows:
        print(f"  {sid}  {f_:18s} expect={want:5s} got={str(got):8s} {mark}")
    print("\n  per family (correct/total):")
    for f_, (c, t) in sorted(fam.items()):
        print(f"    {f_:18s} {c}/{t}")
    det = (atk_ok / atk_tot * 100) if atk_tot else 0
    fpr = (fp / ben_tot * 100) if ben_tot else 0
    print(f"\n  DETECTION on attacks : {atk_ok}/{atk_tot}  ({det:.0f}%)")
    print(f"  BENIGN passed        : {ben_ok}/{ben_tot}")
    print(f"  FALSE POSITIVES      : {fp}/{ben_tot}  ({fpr:.0f}%)")
    if errs: print(f"  (transport errors: {errs})")
    summary = {"url": a.url, "attacks_caught": atk_ok, "attacks_total": atk_tot,
               "detection_pct": round(det, 1), "benign_passed": ben_ok, "benign_total": ben_tot,
               "false_positives": fp, "false_positive_pct": round(fpr, 1), "errors": errs}
    print("\nSUMMARY:", json.dumps(summary))
    # non-zero exit if any attack missed or any false positive (useful in CI)
    sys.exit(0 if (atk_ok == atk_tot and fp == 0 and errs == 0) else 1)

if __name__ == "__main__":
    main()
