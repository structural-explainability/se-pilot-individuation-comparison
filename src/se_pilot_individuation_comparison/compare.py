"""Compare explicitly aligned propositions without inferring scientific correctness."""

from hashlib import sha256
import json
from pathlib import Path
from typing import Any

from .validate import validate_case

SOURCE_INPUTS = (
    "scope.toml",
    "sources.toml",
    "alignment.toml",
    "accounts/epa.toml",
    "accounts/summit.toml",
)


def input_hashes(case_dir: Path) -> dict[str, str]:
    """Identify exactly which bytes a generated comparison consumed."""
    return {
        path: sha256((case_dir / path).read_bytes()).hexdigest()
        for path in SOURCE_INPUTS
    }


def compare_case(data: dict[str, Any]) -> dict[str, Any]:
    """Return preliminary aligned-claim differences with explicit limitation flags."""
    errors = validate_case(data)
    if errors:
        raise ValueError("Invalid case:\n" + "\n".join(errors))
    indexed = {
        name: {claim["id"]: claim for claim in record["claims"]}
        for name, record in data["accounts"].items()
    }
    results: list[dict[str, Any]] = []
    for pair in data["alignment"]["pairs"]:
        left = indexed[pair["left_account"]][pair["left_claim"]]
        right = indexed[pair["right_account"]][pair["right_claim"]]
        limitations: list[str] = []
        if pair["status"] == "not_comparable":
            results.append(
                {
                    "pair_id": pair["id"],
                    "question_id": pair["question_id"],
                    "comparison": "not_comparable",
                    "witness_status": "explicit_noncomparison",
                    "left": {
                        "account": pair["left_account"],
                        "claim": pair["left_claim"],
                    },
                    "right": {
                        "account": pair["right_account"],
                        "claim": pair["right_claim"],
                    },
                    "limitations": [pair["noncomparability_reason"]],
                    "interpretation_limit": (
                        "No proposition equality or difference is inferred across "
                        "incompatible meanings."
                    ),
                }
            )
            continue
        if (
            pair["status"] != "reviewed"
            or data["alignment"]["alignment"]["status"] != "reviewed"
        ):
            limitations.append("alignment_not_independently_reviewed")
        for side, claim in (("left", left), ("right", right)):
            if claim["status"] != "audited":
                limitations.append(f"{side}_claim_not_source_audited")
            if claim["evidence_class"] != "party_primary":
                limitations.append(f"{side}_claim_not_from_party_primary_source")
        for name in (pair["left_account"], pair["right_account"]):
            if not data["accounts"][name]["account"].get(
                "primary_source_review_completed", False
            ):
                limitations.append(f"{name}_primary_source_review_incomplete")
        relation = (
            "recorded_agreement"
            if left["answer"] == right["answer"]
            else "recorded_difference"
        )
        results.append(
            {
                "pair_id": pair["id"],
                "question_id": pair["question_id"],
                "comparison": relation,
                "witness_status": "provisional"
                if limitations
                else "ready_for_external_review",
                "left": {
                    "account": pair["left_account"],
                    "claim": pair["left_claim"],
                    "answer": left["answer"],
                    "source_ids": left["source_ids"],
                    "locator": left["locator"],
                },
                "right": {
                    "account": pair["right_account"],
                    "claim": pair["right_claim"],
                    "answer": right["answer"],
                    "source_ids": right["source_ids"],
                    "locator": right["locator"],
                },
                "limitations": limitations,
                "interpretation_limit": (
                    "A difference of attributed answers is not a causal explanation, "
                    "adjudication, proof of regulatory source partitions, or strict identity claim."
                ),
            }
        )
    return {
        "case_id": data["scope"]["case"]["id"],
        "method": "aligned_binary_proposition_baseline_v1",
        "scientific_adequacy": "OPEN",
        "independent_validation": "NOT_COMPLETED",
        "comparisons": results,
    }


def render_report(result: dict[str, Any]) -> str:
    """Render a conservative human-readable representation of the JSON output."""
    lines = [
        f"# Case comparison: {result['case_id']}",
        "",
        "**Status: PROVISIONAL / NOT SCIENTIFICALLY VALIDATED.**",
        "",
        f"Method: `{result['method']}`. This compares attributed binary propositions only.",
        "",
    ]
    for item in result["comparisons"]:
        lines.extend(
            [
                f"## {item['pair_id']}",
                "",
                (
                    f"- Recorded outcome: `{item['comparison']}`; "
                    f"witness status: `{item['witness_status']}`."
                ),
                f"- {item['left']['account']}: "
                + (
                    f"`{item['left']['answer']}` — sources: "
                    f"{', '.join(item['left']['source_ids'])}."
                    if "answer" in item["left"]
                    else "no comparison attempted."
                ),
                f"- {item['right']['account']}: "
                + (
                    f"`{item['right']['answer']}` — sources: "
                    f"{', '.join(item['right']['source_ids'])}."
                    if "answer" in item["right"]
                    else "no comparison attempted."
                ),
                "- Outstanding conditions: "
                + (", ".join(item["limitations"]) or "none in this structural precheck")
                + ".",
                f"- Limit: {item['interpretation_limit']}",
                "",
            ]
        )
    lines.extend(
        [
            "No scientific adequacy, correctness of either legal position, or theoretical contribution is established by this output.",
            "",
        ]
    )
    return "\n".join(lines)


def save_result(
    result: dict[str, Any], output_dir: Path, *, force: bool = False
) -> None:
    """Write deterministic artifacts without overwriting results accidentally."""
    destinations = (output_dir / "comparison.json", output_dir / "report.md")
    if not force and any(p.exists() for p in destinations):
        raise FileExistsError(
            "Comparison output already exists; refuse overwrite without --force"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    destinations[0].write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    destinations[1].write_text(render_report(result), encoding="utf-8")
