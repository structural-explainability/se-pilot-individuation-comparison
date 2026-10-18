"""Engineering tests for conservative, deterministic comparison behavior."""

from copy import deepcopy
from pathlib import Path

import pytest

from se_pilot_individuation_comparison.compare import (
    compare_case,
    input_hashes,
    render_report,
    save_result,
)
from se_pilot_individuation_comparison.load import load_case

ROOT = Path(__file__).resolve().parents[1] / "cases" / "summit-petroleum"


def test_provisional_difference_is_reported_without_scientific_approval() -> None:
    result = compare_case(load_case(ROOT))
    pair = result["comparisons"][0]
    assert pair["comparison"] == "recorded_difference"
    assert pair["witness_status"] == "provisional"
    assert "right_claim_not_from_party_primary_source" in pair["limitations"]
    assert result["scientific_adequacy"] == "OPEN"


def test_agreement_does_not_become_identity_claim() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["answer"] = True
    result = compare_case(case)
    assert result["comparisons"][0]["comparison"] == "recorded_agreement"
    assert "strict identity claim" in render_report(result)


def test_reject_unaligned_questions() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["question_id"] = "something_else"
    with pytest.raises(ValueError, match="Invalid case"):
        compare_case(case)


def test_source_inputs_are_sha256() -> None:
    values = input_hashes(ROOT)
    assert all(len(value) == 64 for value in values.values())
    assert "accounts/summit.toml" in values


def test_output_is_deterministic_and_refuses_implicit_overwrite(tmp_path: Path) -> None:
    result = compare_case(load_case(ROOT))
    save_result(result, tmp_path)
    first = (tmp_path / "comparison.json").read_bytes()
    with pytest.raises(FileExistsError):
        save_result(result, tmp_path)
    save_result(result, tmp_path, force=True)
    assert first == (tmp_path / "comparison.json").read_bytes()


def test_explicit_incompatible_comparison_is_reported_not_invented() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["question_id"] = "different_question"
    pair = case["alignment"]["pairs"][0]
    pair["status"] = "not_comparable"
    pair["noncomparability_reason"] = "The claims answer different questions."
    result = compare_case(case)
    assert result["comparisons"][0]["comparison"] == "not_comparable"
    assert "answer" not in result["comparisons"][0]["left"]
