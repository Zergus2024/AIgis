# Funding AIgis

AIgis is in an open **test / demo phase**: the gate is exposed for red-teaming, failures are collected
and fixed in the open (see [`Test_AI_failures.md`](Test_AI_failures.md)), and the goal is to grow it into
a platform of **defensive architectures against AI errors** — not only data exfiltration, but the wider
class of unsafe / unjustified AI action.

## Ways to support

| Channel | For | Status |
|---|---|---|
| **GitHub Sponsors / Ko-fi** | individuals who want to back the research + the public demo platform | the fastest, lowest-friction way to help now |
| **Research grants** | AI-safety funders (non-dilutive) | aligns with the published principle ([Layered Self-Regulation](paper/Layered_Self_Regulation.pdf)) |
| **Partnerships** | Notion (Security & Compliance / Technology), and integration partners (see [docs/FRAMEWORKS.md](docs/FRAMEWORKS.md)) | keep AIgis a closed product that *integrates* with your stack |
| **Equity / pilots** | investors and design-partner companies | for serious commitments; contact directly |

## What funding enables
- Hardening the gate beyond surface heuristics (the residual semantic bypasses in the failure log).
- New defensive architectures: hallucinated commitments, premature autonomy, confused-deputy, tool/connector abuse.
- **Independent validation** — funding reproducible third-party red-team / audit (we already ship a
  black-box [`benchmark/`](benchmark) so anyone can verify behavior without seeing the engine).
- Persistent infrastructure (stable endpoints, throughput, SLAs).

## Why back a closed-core project
The *principle* is open and citable; the *engine* is proprietary (trade-secret). Effectiveness is shown
by **reproducible evidence, not by exposing the mechanism** — the standard posture for security products
(IDS/IPS, fraud detection). Your support funds the evidence loop and the platform, not a giveaway of the IP.

## One-pager
For the short investor/partner/grant pitch see [PITCH.md](PITCH.md).

## Contact
Ivan Andrescov — zergus2024@gmail.com · https://www.linkedin.com/in/zergus_j

> To enable the GitHub **Sponsor** button on this repo, turn on GitHub Sponsors for the account and add
> the handle to [`.github/FUNDING.yml`](.github/FUNDING.yml).
