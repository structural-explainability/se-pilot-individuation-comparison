"""Engineering tests of manifest record integrity, not adequacy tests."""

from copy import deepcopy
from pathlib import Path

from se_pilot_individuation_comparison.load import load_case
from se_pilot_individuation_comparison.validate import validate_case

ROOT = Path(__file__).resolve().parents[1] / "cases" / "summit-petroleum"


def test_starter_case_has_valid_record_structure() -> None:
    assert validate_case(load_case(ROOT)) == []


def test_missing_evidence_is_rejected() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["source_ids"] = ["missing"]
    assert any("unknown source ID" in error for error in validate_case(case))


def test_missing_source_locator_is_rejected() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["locator"] = ""
    assert any("needs a source locator" in error for error in validate_case(case))


def test_incompatible_questions_cannot_be_aligned() -> None:
    case = deepcopy(load_case(ROOT))
    case["accounts"]["summit"]["claims"][0]["question_id"] = "different_question"
    assert any("differs from right claim" in error for error in validate_case(case))


def test_unknown_claim_cannot_be_aligned() -> None:
    case = deepcopy(load_case(ROOT))
    case["alignment"]["pairs"][0]["right_claim"] = "invented_claim"
    assert any(
        "references unknown right claim" in error for error in validate_case(case)
    )
