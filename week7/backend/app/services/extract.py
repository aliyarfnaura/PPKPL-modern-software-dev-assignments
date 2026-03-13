import re
from dataclasses import dataclass


@dataclass
class ExtractedActionItem:
    """A single extracted action item with optional metadata."""

    text: str
    keyword: str
    deadline: str | None = None
    owner: str | None = None


# ---------------------------------------------------------------------------
# Keyword patterns (matched against the lowercased line)
# ---------------------------------------------------------------------------
_KEYWORD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("todo", re.compile(r"\btodo\b\s*:?")),
    ("action", re.compile(r"\baction\b\s*:?")),
    ("follow up", re.compile(r"\bfollow\s*-?\s*up\b\s*:?")),
    ("need to", re.compile(r"\bneeds?\s+to\b")),
]

# ---------------------------------------------------------------------------
# Deadline patterns (matched against the original-cased line)
# ---------------------------------------------------------------------------
_DAY_NAMES = r"monday|tuesday|wednesday|thursday|friday|saturday|sunday"
_MONTH_NAMES = (
    r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?"
    r"|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
)

_DEADLINE_PATTERNS: list[re.Pattern[str]] = [
    # "by Monday", "by Friday"
    re.compile(rf"\bby\s+({_DAY_NAMES})", re.IGNORECASE),
    # "by Jan 15", "by January 15"
    re.compile(rf"\bby\s+({_MONTH_NAMES})\s+\d{{1,2}}", re.IGNORECASE),
    # ISO-style: "by 2024-01-15"
    re.compile(r"\bby\s+\d{4}-\d{2}-\d{2}"),
    # "due: ...", "deadline: ..."
    re.compile(r"\b(?:due|deadline)\s*:\s*\S+", re.IGNORECASE),
    # "before tomorrow", "by end of week", "by next week"
    re.compile(
        r"\b(?:by|before)\s+(?:tomorrow|end\s+of\s+\w+|next\s+\w+)",
        re.IGNORECASE,
    ),
]

# ---------------------------------------------------------------------------
# Owner / responsible-entity patterns
# ---------------------------------------------------------------------------
_OWNER_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"@(\w+)"),
    re.compile(r"\bassigned\s+to\s+(\w+)", re.IGNORECASE),
    re.compile(r"\bowner\s*:\s*(\w+)", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _match_keyword(line_lower: str) -> str | None:
    """Return the matched keyword label, or *None* if the line is not actionable."""
    if line_lower.rstrip().endswith("!"):
        return "urgent"
    for label, pattern in _KEYWORD_PATTERNS:
        if pattern.search(line_lower):
            return label
    return None


def _extract_deadline(line: str) -> str | None:
    """Return the first deadline expression found in *line*, or *None*."""
    for pattern in _DEADLINE_PATTERNS:
        m = pattern.search(line)
        if m:
            return m.group(0).strip()
    return None


def _extract_owner(line: str) -> str | None:
    """Return the first responsible entity found in *line*, or *None*."""
    for pattern in _OWNER_PATTERNS:
        m = pattern.search(line)
        if m:
            return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def extract_action_items(text: str) -> list[ExtractedActionItem]:
    """Extract action items from free-form text.

    Each returned item carries the original text, the matched keyword,
    and optional *deadline* / *owner* metadata when detected.
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[ExtractedActionItem] = []
    for line in lines:
        keyword = _match_keyword(line.lower())
        if keyword is None:
            continue
        results.append(
            ExtractedActionItem(
                text=line,
                keyword=keyword,
                deadline=_extract_deadline(line),
                owner=_extract_owner(line),
            )
        )
    return results

