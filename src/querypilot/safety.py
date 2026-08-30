"""Safety policies for agent-generated database work."""

import re


class UnsafeQueryError(ValueError):
    """Raised when SQL is not safely read-only."""


_FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|alter|create|replace|truncate|attach|detach|pragma|vacuum)\b",
    re.IGNORECASE,
)


def validate_read_only_sql(query: str) -> str:
    normalized = query.strip().rstrip(";").strip()
    if not normalized:
        raise UnsafeQueryError("Query cannot be empty")
    if ";" in normalized:
        raise UnsafeQueryError("Multiple SQL statements are not allowed")
    if not re.match(r"^(select|with)\b", normalized, re.IGNORECASE):
        raise UnsafeQueryError("Only SELECT and WITH queries are allowed")
    if _FORBIDDEN.search(normalized):
        raise UnsafeQueryError("Query contains a forbidden SQL operation")
    return normalized
