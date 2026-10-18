# Protocol — Individuation Account Comparison Pilot

**Status:** draft; not frozen; no independent adequacy result.

## Primary scientific question

Can two independently documented, substantively different accounts of the same individuation-relevant regulatory question be represented and compared without presupposing that either account is authoritative, silently inventing common objects, or overstating what a difference witness explains?

## Target and limits

First case: *Summit Petroleum Corp. v. EPA* (6th Cir. 2012). Target: competing interpretations of whether functional interrelatedness is a permitted consideration for the regulatory adjacency condition. The first comparison is **an interpretive-commitment comparison**, not a verified partition of source units, a biological/physical individuation criterion, or a strict identity judgment.

The court case is historical and the outcome is public. We cannot honestly describe comparison to its opinion as independently held-out evidence. Summit's original brief is a missing primary source at setup. Until independently obtained and audited, Summit's position is flagged `court_reported`, and any associated difference is `provisional`.

## Source authority by surface

- Party's own contemporaneous filings/agency determination: strongest evidence of that **party's position**.
- Governing historical regulation: authority for what the enacted legal text says; not an automatic resolution of contested interpretation.
- Court majority/dissent: authority for judicial disposition and a secondary description of party positions; **not** a blind validation source when already used in account construction.
- SE theory: supplies formal abstractions, not independent facts about legal or institutional identities.

## Procedure and freeze points

1. Inventory each primary document; record URL, issue/date, source role, stable identifiers, local preserved checksum if available, and precise locators.
2. Independently transcribe the two party records. Record both assertions and uncertainty. Do not infer full partitions, edges, causal motives, or judgments not present in documents.
3. State the common question and units; justify every `alignment.toml` pair. When carriers/settings are incompatible, return **not comparable**, not an invented mapping.
4. Freeze the case input commit SHA, sources, mappings, comparator revision, acceptance criteria and excluded validation documents in a dated study record **before** the scientific run.
5. Run the frozen comparator; preserve JSON, report, input hashes and CLI versions. Software tests establish engineering behavior only.
6. Obtain independent, adversarial source-only review **without exposing the generated report**; then adversarial witness review in a separate fresh context. Do not expose earlier reviewers' conclusions to later reviewers.
7. Compare independent findings to the frozen result. Report attribution errors, missing claims, incomparable representations, overclaimed causality, and non-findings.
8. Perform a second-domain holdout after freezing the procedure; the original Summit legal case alone cannot establish generalization.

## Failure and stopping rules

- Incorrect source attribution, evidence fabricated or inferred from silence: **fail fidelity**.
- Divergent carrier definitions with no justified correspondence: **not comparable**; success only if reported accurately.
- Claim difference derived only from self-authored labels with no attributable support: **insufficient evidence**.
- Reviewer's disagreement with a formal witness supported by the documents: investigate; do not silently amend evidence or code in the frozen record.
- Correct extraction of a difference alone: **not** a validated theoretical contribution.

## Protocols

- https://github.com/structural-explainability/se-protocols-research/blob/main/protocols/source-audit/SKILL.md
- https://github.com/structural-explainability/se-protocols-research/blob/main/protocols/independent-review/SKILL.md
- https://github.com/structural-explainability/se-protocols-research/blob/main/protocols/theory-construction/SKILL.md
- https://github.com/structural-explainability/se-protocols-research/blob/main/protocols/theory-acceptance/SKILL.md
