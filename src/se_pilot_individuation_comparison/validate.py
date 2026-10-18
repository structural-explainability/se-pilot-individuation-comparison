"""Check record integrity; never certify scientific or legal correctness."""

from typing import Any

ALLOWED_EVIDENCE = {"party_primary", "court_reported"}
ALLOWED_STATUSES = {"provisional", "audited"}


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_case(data: dict[str, Any]) -> list[str]:
    """Return errors; no successful check implies that a claim is warranted."""
    errors: list[str] = []
    scope = data.get("scope", {}).get("case", {})
    if not _is_nonempty_string(scope.get("question")):
        errors.append("scope.case.question is required")
    if not _is_nonempty_string(scope.get("id")):
        errors.append("scope.case.id is required")

    source_records = data.get("sources", {}).get("sources", [])
    if not isinstance(source_records, list):
        errors.append("sources must be a list")
        source_records = []
    source_ids: set[str] = set()
    for source in source_records:
        sid = source.get("id")
        if not _is_nonempty_string(sid) or sid in source_ids:
            errors.append(f"source id is missing or duplicated: {sid!r}")
        else:
            source_ids.add(sid)
        if not _is_nonempty_string(source.get("url")) or not source["url"].startswith(
            "https://"
        ):
            errors.append(f"source {sid!r} must have an HTTPS URL")

    accounts = data.get("accounts", {})
    claims_by_account: dict[str, dict[str, dict[str, Any]]] = {}
    for account_name in ("epa", "summit"):
        record = accounts.get(account_name)
        if not isinstance(record, dict):
            errors.append(f"missing account {account_name}")
            continue
        if record.get("account", {}).get("id") != account_name:
            errors.append(f"account id must be {account_name}")
        claims = record.get("claims", [])
        if not isinstance(claims, list) or not claims:
            errors.append(f"{account_name} must declare at least one claim")
            continue
        indexed: dict[str, dict[str, Any]] = {}
        for claim in claims:
            cid = claim.get("id")
            if not _is_nonempty_string(cid) or cid in indexed:
                errors.append(f"{account_name} claim missing or duplicate id: {cid!r}")
                continue
            indexed[cid] = claim
            if not _is_nonempty_string(claim.get("question_id")):
                errors.append(f"{account_name}.{cid} missing question_id")
            if type(claim.get("answer")) is not bool:
                errors.append(f"{account_name}.{cid} answer must be boolean")
            if claim.get("evidence_class") not in ALLOWED_EVIDENCE:
                errors.append(f"{account_name}.{cid} unsupported evidence_class")
            if claim.get("status") not in ALLOWED_STATUSES:
                errors.append(f"{account_name}.{cid} unsupported status")
            if not _is_nonempty_string(claim.get("assertion")):
                errors.append(f"{account_name}.{cid} needs an attributed assertion")
            if not _is_nonempty_string(claim.get("locator")):
                errors.append(f"{account_name}.{cid} needs a source locator")
            refs = claim.get("source_ids")
            if not isinstance(refs, list) or not refs:
                errors.append(f"{account_name}.{cid} needs source IDs")
            else:
                for sid in refs:
                    if sid not in source_ids:
                        errors.append(
                            f"{account_name}.{cid} unknown source ID: {sid!r}"
                        )
        claims_by_account[account_name] = indexed

    alignment = data.get("alignment", {})
    if alignment.get("alignment", {}).get("status") not in {"proposed", "reviewed"}:
        errors.append("alignment.status must be proposed or reviewed")
    pairs = alignment.get("pairs", [])
    if not isinstance(pairs, list) or not pairs:
        errors.append("alignment must declare at least one pair")
        return errors
    seen: set[str] = set()
    for pair in pairs:
        pid = pair.get("id")
        if not _is_nonempty_string(pid) or pid in seen:
            errors.append(f"alignment pair missing or duplicate id: {pid!r}")
            continue
        seen.add(pid)
        if not _is_nonempty_string(pair.get("justification")):
            errors.append(f"alignment pair {pid} needs justification")
        if pair.get("status") not in {"proposed", "reviewed", "not_comparable"}:
            errors.append(f"alignment pair {pid} has invalid status")
        if pair.get("status") == "not_comparable" and not _is_nonempty_string(
            pair.get("noncomparability_reason")
        ):
            errors.append(f"alignment pair {pid} needs noncomparability_reason")
        for prefix in ("left", "right"):
            account_name = pair.get(f"{prefix}_account")
            claim_id = pair.get(f"{prefix}_claim")
            if (
                account_name not in claims_by_account
                or claim_id not in claims_by_account.get(account_name, {})
            ):
                errors.append(f"alignment {pid} references unknown {prefix} claim")
            else:
                question = claims_by_account[account_name][claim_id].get("question_id")
                if (
                    pair.get("status") != "not_comparable"
                    and pair.get("question_id") != question
                ):
                    errors.append(
                        f"alignment {pid} differs from {prefix} claim question_id"
                    )
        if pair.get("left_account") == pair.get("right_account"):
            errors.append(f"alignment {pid} compares an account to itself")
    return errors
