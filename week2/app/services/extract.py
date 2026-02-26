"""
Action item extraction: heuristic (rule-based) and LLM-based.

- extract_action_items(): rule-based parsing of bullets, keywords, checkboxes.
- extract_action_items_llm(): Ollama LLM extraction; returns [] on empty input or parse/API errors.
  On Ollama model/API errors (e.g. model not found), raises LLMUnavailableError so the API can return 503.
"""
from __future__ import annotations

import json
import logging
import os
import re
from typing import List

from dotenv import load_dotenv
from ollama import chat
from ollama._types import ResponseError as OllamaResponseError

load_dotenv()

# Model name: use OLLAMA_MODEL env var if set, else default to llama3.1
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")
logger = logging.getLogger(__name__)

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    """Extract action items from text using bullet/keyword/checkbox heuristics and optional imperative detection."""
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


class LLMUnavailableError(Exception):
    """Raised when the Ollama model is not available (e.g. not installed or Ollama not running)."""


def extract_action_items_llm(text: str) -> List[str]:
    """
    Extract action items from text using an LLM (Ollama).
    Returns a list of strings. On empty input or invalid JSON response, returns an empty list.
    On Ollama API errors (e.g. model not found), logs and raises LLMUnavailableError.
    """
    if not text or not text.strip():
        return []

    try:
        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Extract all action items, tasks, or to-dos from the user's text. Return ONLY a valid JSON array of strings, one string per action item. No other text or explanation.",
                },
                {"role": "user", "content": text.strip()},
            ],
            format="json",
        )
        raw = response.get("message", {}).get("content", "")
        if not raw:
            return []
        parsed = json.loads(raw)
        if not isinstance(parsed, list):
            return []
        return [str(item).strip() for item in parsed if str(item).strip()]
    except OllamaResponseError as e:
        # Model not found, Ollama not running, or other API error; log and re-raise so API can return 503.
        logger.error(
            "Ollama error (model not found or not running): %s (status %s)",
            getattr(e, "message", str(e)),
            getattr(e, "status_code", "?"),
        )
        raise LLMUnavailableError(
            "LLM model not available. Make sure Ollama is running and the model is installed."
        ) from e
    except (json.JSONDecodeError, KeyError, TypeError):
        # LLM returned invalid JSON or unexpected structure; return empty list (documented behavior).
        return []
