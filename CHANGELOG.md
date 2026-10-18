# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-10-18

### Added

- Initial

---

## Notes on Versioning and Releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible features
  - **PATCH** - fixes, documentation, tests, tooling
- Versions are driven by git tags. Tag `vX.Y.Z` to release.

### Freezes

- Software releases and research freezes are separate lifecycle events.
- A new software release does not automatically require a new research freeze.
- A new research freeze is required only when the applicable frozen scientific
  artifacts or execution conditions change under the study protocol.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. `CHANGELOG.md` - add section, move unreleased entries, update links
1.3. `pyproject.toml` - update build system `fallback-version`

### Task 2. Validate

```shell
uvx pup-clean --delete
npx markdownlint-cli2 --fix
uvx se-manifest-schema validate-manifest --strict
uvx cffconvert --validate
.\sit.ps1

# Update GitHub Actions and pin all action references to immutable SHAs
uvx gha-tools autoupdate --pin=all --write .github/workflows

# Then audit the resulting GitHub configuration for security findings
uvx zizmor@latest .github/
```

### Task 3. Commit, push, tag

```shell
git add -A
git commit -m "Prepare X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

A software release may be created before Freeze 02 is established.

A software release tag does not establish Freeze 02 and does not prevent
additional pre-freeze work.
For changes before Freeze 02, make, validate, and commit those changes normally.

Freeze 02 is established separately by the research-freeze procedure below
against the exact committed pre-freeze state.
A final software release tag may also be created for that state,
but the software tag and the research freeze
remain separate lifecycle events.

## Research Freeze Procedure

Research freezes are deliberate experimental boundaries and are not created
automatically as part of every software release.

### First Commitment/Evaluator Freeze

The first commitment/evaluator freeze is created after the applicable
scientific artifacts have been reviewed, validated, and committed.

Prepare the committed pre-freeze state:

```shell
npx markdownlint-cli2 --fix
uvx se-manifest-schema validate-manifest --strict
uvx cffconvert --validate
.\sit.ps1

uv run python -m comparison_test.fixtures.build_and_selftest

git add -A
git commit -m "Prepare commitment/evaluator freeze"

# Regenerate and verify the synthetic fixture against the committed state
uv run python -m comparison_test.fixtures.build_and_selftest

git status
# must report a clean working tree before creating the freeze.
```

The working tree must be clean before creating the freeze.
If rerunning the self-test modifies either generated fixture file, do not
create the freeze.
Review the difference, commit the corrected pre-freeze
state, rerun the self-test, and confirm that the working tree remains clean.

After confirming clean, create the freeze record explicitly:

```shell
.\freeze_01.ps1
```

Review the generated record at `contracts/FREEZE_01_COMMITMENT_EVALUATOR.md`

Commit the freeze record:

```shell
git add contracts/FREEZE_01_COMMITMENT_EVALUATOR.md
git commit -m "Record commitment/evaluator freeze"
```

Do not overwrite `contracts/FREEZE_01_COMMITMENT_EVALUATOR.md`.

Additional tests and documentation may be added without breaking this freeze
when they only verify or explain the frozen behavior.

If a frozen scientific artifact must change, follow the freeze-break procedure
in `docs/en/run.md` and create a new applicable freeze.

### Freeze

Review the resulting pre-freeze state, then run the normal repository
validation:

```powershell
.\sit.ps1
```

Review all changes before committing.

```powershell
git add -A
git commit -m "Prepare generalization freeze"
git push -u origin main
```

A software release tag may be created for this exact pre-freeze state if
desired, using the normal release procedure above.
The software tag is useful provenance but is not itself Freeze 02.
After committing the final pre-freeze state, do not rerun `run.ps1`.
Verify the committed state without rebuilding it:

```powershell
uv run --locked python -m comparison_test.generalization.verification.verify_05_freeze_02

git status
```

The verification must succeed and `git status` must report a clean working
tree before Freeze 02 is created.

If verification fails or the working tree is not clean, do not create
Freeze 02.
Correct the pre-freeze state, commit the correction, rerun the verification,
and again confirm a clean working tree.

#### Establish Freeze 02

After the final pre-freeze state is committed, verified, and clean, establish
Freeze 02 explicitly:

```powershell
.\freeze_02.ps1
```

The Freeze 02 procedure must not execute a generalization transformation or
inspect any generalization transformation or evaluator output.
Review the finalized freeze record at:

```text
contracts/FREEZE_02_GENERALIZATION.md
```

Confirm that it records the intended corpus, execution conditions, environment,
artifact hashes, limitations, and applicable Freeze 01 commitment/evaluator.
Commit the Freeze 02 record:

```powershell
git add contracts/FREEZE_02_GENERALIZATION.md
git commit -m "Record generalization freeze"
git push -u origin main
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
```

## Links

[Unreleased]: https://github.com/structural-explainability/se-pilot-individuation-comparison/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/structural-explainability/se-pilot-individuation-comparison/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
