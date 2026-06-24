# AIgis reproducible red-team benchmark

The point of this folder: **let anyone verify the gate's effectiveness without seeing its engine.** You
run a public scenario set against a live AIgis endpoint and measure detection + false positives
yourself. You verify *behavior*, not *mechanism*.

## What's here
- [`scenarios.jsonl`](scenarios.jsonl) - a labeled scenario set. Each line:
  `{id, family, expect: block|allow, request}`. **The label describes the scenario's intent**
  (is it an attack that should be held, or a benign action that should pass) - it does **not** encode
  how the gate decides. Attack techniques used are publicly documented (injection→exfiltration,
  destructive commands, obfuscation).
- [`run_benchmark.py`](run_benchmark.py) - stdlib runner. Sends each scenario to `/api/gate` and scores
  the verdicts: detection rate on attacks, false-positive rate on benign controls, per-family breakdown.

## Run it
```bash
# 1. register at the demo URL to get a key (aig_...)
# 2. run the benchmark against the live gate (black box):
python run_benchmark.py --url https://YOUR-DEMO-URL --key aig_xxx
```
Exit code is `0` only if every attack is held AND there are zero false positives (CI-friendly).

## What it proves (and what it does not)
- **Proves:** the gate, as a black box, holds the attack scenarios and passes the benign ones, with a
  measurable false-positive rate - reproducibly, by you, against the live endpoint.
- **Does not reveal:** the gate's decision principle, thresholds, formulas, or verification layer. The
  runner never inspects the engine; it only observes input→verdict.

This is the standard posture for security products (IDS/IPS, fraud detection): **demonstrate
effectiveness without disclosing the mechanism.** Extend the set with your own scenarios and re-run -
that is exactly the independent validation a reviewer should want.

> Note: the public demo endpoint runs an **illustrative** gate (the production engine is proprietary).
> The benchmark is the methodology; point it at whichever deployment you are evaluating.
