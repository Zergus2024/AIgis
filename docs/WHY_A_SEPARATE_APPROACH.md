# Why a separate approach is required

There is a crowded field of AI-agent defenses. They are useful — and they leave one gap structurally
unaddressed. This page explains the gap **without** disclosing how GroundGate fills it (the mechanism is
proprietary; the principle is published: [Layered Self-Regulation](../paper/Layered_Self_Regulation.pdf)).

## The existing camps — and what each one cannot do

**1. Action firewalls / policy enforcement** (open-source agent firewalls, tool-call interceptors,
MCP-poisoning scanners, RBAC/PII-masking gateways).
They block **known-bad actions** — exfiltration channels, dangerous commands, poisoned tool definitions.
Necessary, and largely commoditized. But they answer *"is this action on a blocklist / does it match a
known-bad pattern?"* — **not** *"is this action or answer actually justified?"* A confidently wrong
recommendation, a sycophantic agreement, a hallucinated commitment, or a premature autonomous step is
**not a dangerous tool call** — it sails straight through an action firewall.

**2. Internal-signal / logprob methods** (token log-probabilities, entropy, self-consistency,
"the model's own confidence").
These read the model's **internal state** to estimate uncertainty. The structural problem: at the
frontier, **internal confidence decouples from correctness** — models are *confidently* wrong, calibration
drifts, and on closed/hosted APIs the signals are often unavailable or unreliable. A defense built on the
model's own logprobs inherits exactly the failure it is meant to catch. (This is an empirical finding of
the underlying research; the *how* of a working alternative is not disclosed here.)

**3. Training-time alignment** (RLHF, Constitutional AI, beneficial-trait RL).
Shapes the model's disposition. Probabilistic, lives in the weights, steerable by prompts, removable by
fine-tuning — and it does not remove an architectural channel. It lowers the base rate; it does not
guarantee validity. (See [COMPARISON.md](COMPARISON.md).)

## The unaddressed gap

None of the three judges the **validity / justification of an action or answer under unresolved
uncertainty**. Firewalls look at *known-bad actions*; logprob methods look at *the model's own feeling*;
alignment looks at *the model's trained disposition*. The missing question is the important one:

> *Given the evidence available, is this action/answer justified — or is the agent acting confidently
> without sufficient grounds?*

## Why it must be a separate approach

To fill that gap a defense must be **both**:
- **external to the model** — because the model's internal signals fail at the frontier (camp 2), and
  because the guarantee must survive prompting and fine-tuning (camp 3); and
- **beyond action-blocklists** — because the failure is a *judgment*, not a *known-bad pattern* (camp 1).

That is a different axis from everything above — which is why bolting GroundGate's missing piece onto an
existing firewall, a logprob detector, or an aligned model **does not produce it**. The existing tools
are complementary (use them for what they do well); they do not, and by construction cannot, close this
gap. GroundGate is built on that separate axis. **How** it does so is proprietary; **that** it is a distinct,
necessary axis is the point of this page.

## Why the mechanical approaches stall

There is a market signal here. Logprob/internal-signal detectors and pattern/keyword filters are
**evadable** — as anyone can confirm by red-teaming them (see [`../Test_AI_failures.md`](../Test_AI_failures.md),
where even our own surface demo is bypassed by plain-language intent). A defense that can be reworded
around does not earn durable trust or serious contracts; it stays a utility, not a guarantee.

The stable alternative is **grounding against an explicit reference**: compile the set of facts/policies
that *must* hold, and verify the action/answer **against that set** — rather than scanning text for
matches (reworded away in seconds) or trusting the model's *claim* that it checked (a model will happily
say it "read the file" it never opened). Grounding is checkable and repeatable; pattern-matching and
self-report are not. That stability — not another blocklist — is what a real guarantee requires, and
why this is a separate approach rather than a feature bolted onto the existing ones. (The principle is
published; the implementation is not.)
