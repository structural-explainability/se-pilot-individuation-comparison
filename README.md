# SE Pilot: Individuation Account Comparison

[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://structural-explainability.github.io/se-pilot-individuation-comparison/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/structural-explainability/se-pilot-individuation-comparison)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI](https://github.com/structural-explainability/se-pilot-individuation-comparison/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-pilot-individuation-comparison/actions/workflows/ci-python-zensical.yml)
[![Docs Deploy](https://github.com/structural-explainability/se-pilot-individuation-comparison/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/se-pilot-individuation-comparison/actions/workflows/deploy-zensical.yml)

> Source-grounded feasibility pilot for comparing
> genuinely different accounts of what constitutes one regulatory source.

**Status: DRAFT.** Engineering demonstration only.
Scientific adequacy and independent validation remain OPEN.

## Research question

Can Structural Explainability represent two parties'
actual individuation-relevant commitments and identify
a warranted, inspectable disagreement
**without treating either party's interpretation as authoritative or inventing a common ontology**?

The first case is _Summit Petroleum Corp. v. EPA_ (6th Cir. 2012).
It tests disagreement about the regulatory meaning of _adjacent_
in Title V stationary-source aggregation.
It does **not** assume that regulatory aggregation establishes
metaphysical identity or that either position
defines a complete equivalence relation on facilities.

See the [Study Overview](./docs/en/index.md) for the research design,
the [Run Protocol](./docs/en/run.md) for freeze and execution procedures,
and the [Test Guide](./docs/en/test.md) for engineering validation.

## Scope of the initial implementation

The Python runner implements a deliberately **thin baseline**:
a source-traceable comparison of aligned binary propositions.
It detects a recorded difference and its evidence limitations.
It does **not** derive structural wholes,
independently adjudicate warrant,
prove causes of disagreement, implement Lean theory, or
validate the theory's substantive scientific contribution.
Those are targets of the pilot, not achievements of this scaffold.

The EPA record is represented using its public respondent brief.
Summit's initial record relies on the court's report of Summit's argument
because an original Summit filing has not been verified in this starter.
**This makes the example retrospective and partially validation-contaminated.**
The court opinion must not be represented as
an independent held-out validation source for the same proposition.

## Organization

- `study/` - frozen-before-use protocol, acceptance criteria, independent review instructions.
- `cases/summit-petroleum/` - scoped case, provenance, party positions, proposed alignment, and subsequent results/reviews.
- `src/se_pilot_individuation_comparison/` - minimal case reader, validator, comparison and CLI.
- `tests/` - engineering tests, including rejection and noncomparability cases.

## Run locally (PowerShell, Python 3.14+)

```powershell
# Install the locked research environment
uv sync --locked

# Validate source-grounded account records
uv run --locked python -m se_pilot_individuation_comparison validate cases/summit-petroleum

# Produce the comparison and explanation
uv run --locked python -m se_pilot_individuation_comparison compare cases/summit-petroleum --force
# See: cases/summit-petroleum/results

# Do chores
uv run --locked python -m pytest
uv run --locked ruff check .
uv run --locked ty check
```

## Overview

- [README.md](./generalization/README.md)

## Annotations

[.annotations/annotations.md](./.annotations/annotations.md)

## Changelog

[Changelog](./CHANGELOG.md)

## Citation

Citation metadata is available in [CITATION.cff](./CITATION.cff).

## License

[MIT](./LICENSE)

## Repository Manifest

The repository's role, scope, and dependencies are declared in
[SE_MANIFEST.toml](./SE_MANIFEST.toml).
