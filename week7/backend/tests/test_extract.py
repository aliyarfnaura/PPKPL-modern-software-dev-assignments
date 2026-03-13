from backend.app.services.extract import ExtractedActionItem, extract_action_items


def _texts(items: list[ExtractedActionItem]) -> list[str]:
    return [item.text for item in items]


# ------------------------------------------------------------------
# Original behaviour (must keep working)
# ------------------------------------------------------------------
def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    texts = _texts(items)
    assert "TODO: write tests" in texts
    assert "ACTION: review PR" in texts
    assert "Ship it!" in texts


def test_original_keywords_set_correct_keyword_field():
    text = "TODO: write tests\nACTION: review PR\nShip it!"
    items = extract_action_items(text)
    by_text = {item.text: item for item in items}
    assert by_text["TODO: write tests"].keyword == "todo"
    assert by_text["ACTION: review PR"].keyword == "action"
    assert by_text["Ship it!"].keyword == "urgent"


# ------------------------------------------------------------------
# New keyword patterns
# ------------------------------------------------------------------
def test_follow_up_keyword():
    text = "Follow up: check deployment status\nJust a regular note"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0].text == "Follow up: check deployment status"
    assert items[0].keyword == "follow up"


def test_follow_up_hyphenated():
    text = "follow-up with client about contract"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0].keyword == "follow up"


def test_need_to_keyword():
    text = "We need to update the docs before release"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0].keyword == "need to"


def test_needs_to_keyword():
    text = "Team needs to finalize the API spec"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0].keyword == "need to"


# ------------------------------------------------------------------
# Deadline detection
# ------------------------------------------------------------------
def test_deadline_by_day():
    text = "TODO: submit report by Friday"
    items = extract_action_items(text)
    assert items[0].deadline == "by Friday"


def test_deadline_by_date():
    text = "ACTION: deploy release by Jan 15"
    items = extract_action_items(text)
    assert items[0].deadline == "by Jan 15"


def test_deadline_iso_date():
    text = "TODO: complete migration by 2024-03-01"
    items = extract_action_items(text)
    assert items[0].deadline == "by 2024-03-01"


def test_deadline_due():
    text = "TODO: fix bug due: tomorrow"
    items = extract_action_items(text)
    assert items[0].deadline == "due: tomorrow"


def test_deadline_before_tomorrow():
    text = "Action: send invoice before tomorrow"
    items = extract_action_items(text)
    assert items[0].deadline == "before tomorrow"


def test_deadline_by_next_week():
    text = "TODO: prepare slides by next Monday"
    items = extract_action_items(text)
    assert items[0].deadline == "by next Monday"


def test_no_deadline():
    text = "TODO: general cleanup"
    items = extract_action_items(text)
    assert items[0].deadline is None


# ------------------------------------------------------------------
# Owner / responsible-entity detection
# ------------------------------------------------------------------
def test_owner_at_mention():
    text = "TODO: review PR @alice"
    items = extract_action_items(text)
    assert items[0].owner == "alice"


def test_owner_assigned_to():
    text = "Action: update docs assigned to Bob"
    items = extract_action_items(text)
    assert items[0].owner == "Bob"


def test_owner_field():
    text = "TODO: deploy to staging owner: Charlie"
    items = extract_action_items(text)
    assert items[0].owner == "Charlie"


def test_no_owner():
    text = "TODO: general cleanup"
    items = extract_action_items(text)
    assert items[0].owner is None


# ------------------------------------------------------------------
# Combined metadata
# ------------------------------------------------------------------
def test_combined_deadline_and_owner():
    text = "TODO: ship feature by Friday @dave"
    items = extract_action_items(text)
    assert len(items) == 1
    assert items[0].keyword == "todo"
    assert items[0].deadline == "by Friday"
    assert items[0].owner == "dave"


def test_non_actionable_lines_ignored():
    text = "Just a regular note\nNothing to see here"
    items = extract_action_items(text)
    assert items == []

