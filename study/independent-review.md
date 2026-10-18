# Independent review packet instructions

Reference: https://github.com/structural-explainability/se-protocols-research/blob/main/protocols/independent-review/SKILL.md

**Do not treat two agreeing agents as independent unless the information paths were separate.**

## Source-only reviewer

Receive the research question, permitted original documents and source provenance. Do **not** receive extracted accounts, comparator implementation/output, prior reviewers' conclusions, or desired answer. Independently state what each party affirmed, denied, and did not establish, with source locators. Note any incompatibility of scopes or terms. Attempt to find errors or omissions in the candidate question itself.

## Adversarial witness reviewer

In a separate fresh context, receive the frozen inputs, code, output and source originals. Do **not** receive the authors' reasoning transcript or other reviewers' reports. Try to falsify attribution, compatibility, witness fidelity and claims of theoretical significance. Prefer concrete counterexamples.

## Required review record

Capture reviewer/model class, date, fresh-context confirmation, exact prompt, allowed source set, candidate commit SHA, excluded information, prior-review visibility, detected problems, verdict (`ACCEPT`, `ACCEPT WITH NARROWING`, `REJECT`, `INSUFFICIENT BASIS`) and justification. Only compare reviewer reports after each is complete. Human inspection remains required.
