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

- Initial research pilot for comparing independently documented individuation accounts.
- Summit Petroleum case with separate EPA and Summit account records, source inventory,
  scope, and alignment.
- Python validation and comparison commands for attributed binary propositions.
- Machine-readable JSON and human-readable Markdown comparison reports.
- Source provenance, input SHA-256 hashes, and explicit comparison limitations.
- Research protocol, acceptance criteria, and independent-review instructions.
- Automated engineering tests and repository metadata.

### Limitations

- Initial comparison results are provisional.
- Primary-source auditing and independent validation remain incomplete.
- Scientific adequacy and theoretical contribution remain OPEN.
- No Structural Explainability theory validation is claimed.

---

## Notes on Versioning and Releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible features
  - **PATCH** - fixes, documentation, tests, tooling
- Keep project version metadata and release tags consistent.
  Tag `vX.Y.Z` to release.

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
1.3. `pyproject.toml` - update `[project].version`

### Task 2. Validate

```shell
npx markdownlint-cli2 --fix
uvx se-manifest-schema validate-manifest --strict
uvx cffconvert --validate
.\sitsafe.ps1

# Update GitHub Actions and pin all action references to immutable SHAs
uvx gha-tools autoupdate --pin=all --write .github/workflows

# Then audit the resulting GitHub configuration for security findings
uvx zizmor@latest .github/
# one informational is fine
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

## Only As Needed (delete a tag)

```shell
git tag -d vX.Y.Z
git push origin :refs/tags/vX.Y.Z
```

## Links

[Unreleased]: https://github.com/structural-explainability/se-pilot-individuation-comparison/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/structural-explainability/se-pilot-individuation-comparison/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
