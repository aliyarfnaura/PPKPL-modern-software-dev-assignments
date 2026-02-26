import pytest
from unittest.mock import patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ---- extract_action_items_llm (mocked) ----
# Patch where chat is used: week2.app.services.extract.chat

CHAT_PATCH = "week2.app.services.extract.chat"


@patch(CHAT_PATCH)
def test_extract_llm_valid_bullet_style(mock_chat):
    """Valid bullet-style input returns multiple action items."""
    mock_chat.return_value = {
        "message": {"content": '["Buy milk", "Finish homework", "Call mom"]'},
    }
    result = extract_action_items_llm("- Buy milk\n- Finish homework\n- Call mom")
    assert result == ["Buy milk", "Finish homework", "Call mom"]
    mock_chat.assert_called_once()


@patch(CHAT_PATCH)
def test_extract_llm_keyword_prefix(mock_chat):
    """Keyword-prefixed input (e.g. TODO: fix bug) returns extracted item."""
    mock_chat.return_value = {
        "message": {"content": '["fix bug"]'},
    }
    result = extract_action_items_llm("TODO: fix bug")
    assert result == ["fix bug"]
    mock_chat.assert_called_once()


@patch(CHAT_PATCH)
def test_extract_llm_empty_input(mock_chat):
    """Empty or whitespace-only input returns empty list without calling chat."""
    assert extract_action_items_llm("") == []
    assert extract_action_items_llm("   ") == []
    mock_chat.assert_not_called()


@patch(CHAT_PATCH)
def test_extract_llm_invalid_json_returns_empty_list(mock_chat):
    """Invalid JSON in model response returns empty list."""
    mock_chat.return_value = {
        "message": {"content": "not valid json at all"},
    }
    result = extract_action_items_llm("Some task here")
    assert result == []
    mock_chat.assert_called_once()
