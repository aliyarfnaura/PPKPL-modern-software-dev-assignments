"""Tests for pagination and sorting on the /action-items/ endpoint."""

import time


# ── helpers ──────────────────────────────────────────────────────────

def _create_items(client, count: int) -> list[dict]:
    """Create *count* action items and return the JSON responses."""
    items = []
    for i in range(count):
        r = client.post("/action-items/", json={"description": f"Task {i}"})
        assert r.status_code == 201
        items.append(r.json())
        time.sleep(0.05)
    return items


# ── pagination ───────────────────────────────────────────────────────

class TestActionItemsPagination:
    def test_limit_restricts_result_count(self, client):
        _create_items(client, 5)
        r = client.get("/action-items/", params={"limit": 3})
        assert r.status_code == 200
        assert len(r.json()) == 3

    def test_skip_offsets_results(self, client):
        _create_items(client, 5)
        all_items = client.get("/action-items/", params={"sort": "id"}).json()

        r = client.get("/action-items/", params={"skip": 2, "sort": "id"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 3
        assert data[0]["id"] == all_items[2]["id"]

    def test_skip_and_limit_combined(self, client):
        _create_items(client, 6)
        all_items = client.get("/action-items/", params={"sort": "id"}).json()

        r = client.get("/action-items/", params={"skip": 1, "limit": 2, "sort": "id"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 2
        assert data[0]["id"] == all_items[1]["id"]
        assert data[1]["id"] == all_items[2]["id"]

    def test_skip_past_all_results_returns_empty(self, client):
        _create_items(client, 3)
        r = client.get("/action-items/", params={"skip": 100})
        assert r.status_code == 200
        assert r.json() == []

    def test_limit_larger_than_dataset(self, client):
        _create_items(client, 2)
        r = client.get("/action-items/", params={"limit": 100})
        assert r.status_code == 200
        assert len(r.json()) == 2

    def test_limit_exceeds_max_returns_422(self, client):
        """The endpoint caps limit at 200; values above should be rejected."""
        r = client.get("/action-items/", params={"limit": 201})
        assert r.status_code == 422


# ── sorting ──────────────────────────────────────────────────────────

class TestActionItemsSorting:
    def test_sort_by_description_ascending(self, client):
        _create_items(client, 4)
        r = client.get("/action-items/", params={"sort": "description"})
        assert r.status_code == 200
        descs = [i["description"] for i in r.json()]
        assert descs == sorted(descs)

    def test_sort_by_description_descending(self, client):
        _create_items(client, 4)
        r = client.get("/action-items/", params={"sort": "-description"})
        assert r.status_code == 200
        descs = [i["description"] for i in r.json()]
        assert descs == sorted(descs, reverse=True)

    def test_sort_by_created_at_ascending(self, client):
        _create_items(client, 3)
        r = client.get("/action-items/", params={"sort": "created_at"})
        assert r.status_code == 200
        dates = [i["created_at"] for i in r.json()]
        assert dates == sorted(dates)

    def test_sort_by_created_at_descending(self, client):
        _create_items(client, 3)
        r = client.get("/action-items/", params={"sort": "-created_at"})
        assert r.status_code == 200
        dates = [i["created_at"] for i in r.json()]
        assert dates == sorted(dates, reverse=True)

    def test_invalid_sort_field_falls_back_to_default(self, client):
        """An unknown sort field should fall back to -created_at."""
        _create_items(client, 3)
        r = client.get("/action-items/", params={"sort": "nonexistent"})
        assert r.status_code == 200
        dates = [i["created_at"] for i in r.json()]
        assert dates == sorted(dates, reverse=True)


# ── edge cases ───────────────────────────────────────────────────────

class TestActionItemsEdgeCases:
    def test_empty_database_returns_empty_list(self, client):
        r = client.get("/action-items/")
        assert r.status_code == 200
        assert r.json() == []

    def test_completed_filter_with_no_match_returns_empty(self, client):
        _create_items(client, 2)  # all incomplete by default
        r = client.get("/action-items/", params={"completed": True})
        assert r.status_code == 200
        assert r.json() == []

    def test_pagination_with_completed_filter(self, client):
        """Pagination should work together with the completed filter."""
        items = _create_items(client, 4)
        # mark first two as completed
        for it in items[:2]:
            client.put(f"/action-items/{it['id']}/complete")

        r = client.get("/action-items/", params={"completed": True, "limit": 1})
        assert r.status_code == 200
        assert len(r.json()) == 1
        assert r.json()[0]["completed"] is True

    def test_sorting_with_completed_filter(self, client):
        """Sorting should still work when a filter is active."""
        items = _create_items(client, 3)
        for it in items:
            client.put(f"/action-items/{it['id']}/complete")

        r = client.get("/action-items/", params={"completed": True, "sort": "created_at"})
        assert r.status_code == 200
        dates = [i["created_at"] for i in r.json()]
        assert dates == sorted(dates)
