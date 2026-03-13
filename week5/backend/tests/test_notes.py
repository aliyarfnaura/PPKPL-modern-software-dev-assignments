def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 1
    assert len(body["items"]) >= 1
    assert body["page"] == 1
    assert body["page_size"] == 10

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_notes_pagination(client):
    # Create 5 notes
    for i in range(5):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    # Page 1 with page_size=2
    r = client.get("/notes/", params={"page": 1, "page_size": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 2
    assert body["page"] == 1
    assert body["page_size"] == 2

    # Page 3 with page_size=2 → last page with 1 item
    r = client.get("/notes/", params={"page": 3, "page_size": 2})
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 1

    # Page beyond total → empty items
    r = client.get("/notes/", params={"page": 10, "page_size": 2})
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 0

    # Large page_size returns all items
    r = client.get("/notes/", params={"page": 1, "page_size": 100})
    body = r.json()
    assert body["total"] == 5
    assert len(body["items"]) == 5


def test_notes_pagination_invalid_params(client):
    # page < 1 should be rejected
    r = client.get("/notes/", params={"page": 0})
    assert r.status_code == 422

    # page_size < 1 should be rejected
    r = client.get("/notes/", params={"page_size": 0})
    assert r.status_code == 422

    # page_size > 100 should be rejected
    r = client.get("/notes/", params={"page_size": 101})
    assert r.status_code == 422
