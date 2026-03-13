def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert len(body["items"]) == 1
    assert body["page"] == 1
    assert body["page_size"] == 10


def test_action_items_pagination(client):
    for i in range(5):
        client.post("/action-items/", json={"description": f"Task {i}"})

    # Page 1 with page_size=2
    r = client.get("/action-items/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2

    # Page beyond total → empty items
    r = client.get("/action-items/", params={"page": 10, "page_size": 2})
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 0

    # Large page_size returns all
    r = client.get("/action-items/", params={"page": 1, "page_size": 100})
    body = r.json()
    assert len(body["items"]) == 5


def test_action_items_pagination_invalid_params(client):
    r = client.get("/action-items/", params={"page": 0})
    assert r.status_code == 422

    r = client.get("/action-items/", params={"page_size": 0})
    assert r.status_code == 422

    r = client.get("/action-items/", params={"page_size": 101})
    assert r.status_code == 422
