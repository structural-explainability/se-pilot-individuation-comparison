"""Read the pilot's declarative TOML records without changing their meaning."""

from pathlib import Path
import tomllib
from typing import Any


def read_toml(path: Path) -> dict[str, Any]:
    """Return the parsed TOML table; raise for an absent or malformed file."""
    with path.open("rb") as stream:
        return tomllib.load(stream)


def load_case(case_dir: Path) -> dict[str, Any]:
    """Load a case and its two explicitly named account records."""
    return {
        "scope": read_toml(case_dir / "scope.toml"),
        "sources": read_toml(case_dir / "sources.toml"),
        "alignment": read_toml(case_dir / "alignment.toml"),
        "accounts": {
            name: read_toml(case_dir / "accounts" / f"{name}.toml")
            for name in ("epa", "summit")
        },
    }
