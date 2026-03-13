"""Tests for pagination and sorting on the /notes/ endpoint."""

import time


# ── helpers ──────────────────────────────────────────────────────────

def _create_notes(client, count: int) -> list[dict]:
    """Create *count* notes with distinguishable titles and return them."""
    notes = []
    for i in range(count):
        r = client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
        assert r.status_code == 201
        notes.append(r.json())
        # tiny sleep so created_at values are distinct on platforms with
        # low-resolution clocks (e.g. Windows / SQLite)
        time.sleep(0.05)
    return notes


# ── pagination ───────────────────────────────────────────────────────

class TestNotesPagination:
    def test_limit_restricts_result_count(self, client):
        _create_notes(client, 5)
        r = client.get("/notes/", params={"limit": 3})
        assert r.status_code == 200
        assert len(r.json()) == 3

    def test_skip_offsets_results(self, client):
        created = _create_notes(client, 5)
        all_notes = client.get("/notes/", params={"sort": "id"}).json()

        r = client.get("/notes/", params={"skip": 2, "sort": "id"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        assert data[0]["id"] == all_notes[2]["id"]

    def test_skip_and_limit_combined(self, client):
        _create_notes(client, 6)
        all_notes = client.get("/notes/", params={"sort": "id"}).json()

        r = client.get("/notes/", params={"skip": 1, "limit": 2, "sort": "id"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 2
        assert data[0]["id"] == all_notes[1]["id"]
        assert data[1]["id"] == all_notes[2]["id"]

    def test_skip_past_all_results_returns_empty(self, client):
        _create_notes(client, 3)
        r = client.get("/notes/", params={"skip": 100})
        assert r.status_code == 200
        assert r.json() == []

    def test_limit_larger_than_dataset(self, client):
        _create_notes(client, 2)
        r = client.get("/notes/", params={"limit": 100})
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_limit_exceeds_max_returns_422(self, client):
        """The endpoint caps limit at 200; values above should be rejected."""
        r = client.get("/notes/", params={"limit": 201})
        assert r.status_code == 422


# ── sorting ──────────────────────────────────────────────────────────

class TestNotesSorting:
    def test_sort_by_title_ascending(self, client):
        _create_notes(client, 4)
        r = client.get("/notes/", params={"sort": "title"})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert titles == sorted(titles)

    def test_sort_by_title_descending(self, client):
        _create_notes(client, 4)
        r = client.get("/notes/", params={"sort": "-title"})
        assert r.status_code == 200
        titles = [n["title"] for n in r.json()]
        assert titles == sorted(titles, reverse=True)

    def test_sort_by_created_at_ascending(self, client):
        _create_notes(client, 3)
        r = client.get("/notes/", params={"sort": "created_at"})
        assert r.status_code == 200
        dates = [n["created_at"] for n in r.json()]
        assert dates == sorted(dates)

    def test_sort_by_created_at_descending(self, client):
        _create_notes(client, 3)
        r = client.get("/notes/", params={"sort": "-created_at"})
        assert r.status_code == 200
        dates = [n["created_at"] for n in r.json()]
        assert dates == sorted(dates, reverse=True)

    def test_invalid_sort_field_falls_back_to_default(self, client):
        """An unknown sort field should fall back to -created_at."""
        created = _create_notes(client, 3)
        r = client.get("/notes/", params={"sort": "nonexistent"})
        assert r.status_code == 200
        dates = [n["created_at"] for n in r.json()]
        assert dates == sorted(dates, reverse=True)


# ── edge cases ───────────────────────────────────────────────────────

class TestNotesEdgeCases:
    def test_empty_database_returns_empty_list(self, client):
        r = client.get("/notes/")
        assert r.status_code == 200
        assert r.json() == []

    def test_search_with_no_match_returns_empty(self, client):
        _create_notes(client, 2)
        r = client.get("/notes/", params={"q": "zzz_no_match"})
        assert r.status_code == 200
        assert r.json() == []

    def test_pagination_with_search_filter(self, client):
        """Pagination should work together with the q filter."""
        for i in range(4):
            client.post("/notes/", json={"title": "Match", "content": f"body {i}"})
        client.post("/notes/", json={"title": "Other", "content": "irrelevant"})

        r = client.get("/notes/", params={"q": "Match", "limit": 2})
        assert r.status_code == 200
        assert len(r.json()) == 2
