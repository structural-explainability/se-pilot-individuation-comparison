# Acceptance criteria

**Status: not evaluated.** This is an experiment, not certification of SE.

## Gate 1 — Engineering correctness

- TOML can be parsed and validated without silent field dropping.
- Missing claims/evidence/source locators cannot produce a verified witness.
- Unsupported mappings cannot produce a comparison.
- Outputs are deterministic and carry hashes identifying all compared case inputs.
- Explicitly declared noncomparability is reported as noncomparability without constructing a fictitious witness.
- The CLI and tests pass on the recorded environment.

## Gate 2 — Scientific adequacy (blocks acceptance)

- Each party's account has auditable source locators and independently checked fidelity.
- Source-only reviewers independently recover the material disagreements and note omissions.
- Comparator output aligns with the actual propositions, without claiming legal/physical strict identity or overclaiming causes.
- At least one case can yield a counterexample, correction, or narrowing; reasons for not-comparable and insufficient-evidence outcomes are inspectable.
- Any account derived from a judicial summary rather than its party's source is flagged; that judicial text does not simultaneously count as an independent external validation of it.

## Gate 3 — Theoretical contribution (separate)

A positive contribution needs an explicit, tested demonstration that existing SE notions yield correct, nontrivial constraints or explanations *not already supplied verbatim by the input records*. Reporting a label difference or a row-level diff is not sufficient.

## Dispositions

Record **PASS**, **FAIL**, or **INSUFFICIENT EVIDENCE** separately at each gate. Do not infer Gate 2 or Gate 3 from Gate 1. Scientific theory acceptance remains **OPEN** until independent review and human inspection.

## Beyond the first case

The second case must come from an independently selected domain after comparator and scoring criteria are frozen. Any redesign after looking at that case makes it a development case, not a held-out test.
