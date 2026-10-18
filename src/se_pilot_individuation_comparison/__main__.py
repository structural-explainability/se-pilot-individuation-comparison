"""Command-line entry point for the feasibility pilot."""

import argparse
from pathlib import Path

from .compare import compare_case, input_hashes, save_result
from .load import load_case
from .validate import validate_case


def main() -> int:
    """Validate a case or generate a provisional, source-traceable comparison."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("validate", "compare"))
    parser.add_argument("case_dir", type=Path)
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing, unfrozen results"
    )
    args = parser.parse_args()
    try:
        data = load_case(args.case_dir)
        errors = validate_case(data)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        if args.action == "validate":
            print(
                f"VALID INPUT STRUCTURE: {args.case_dir} (not independent scientific validation)"
            )
            return 0
        result = compare_case(data)
        result["input_sha256"] = input_hashes(args.case_dir)
        save_result(result, args.case_dir / "results", force=args.force)
        print(f"WROTE PROVISIONAL comparison: {args.case_dir / 'results'}")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
