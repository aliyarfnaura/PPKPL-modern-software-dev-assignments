def test_create_and_list_tags(client):
    r = client.post("/tags/", json={"name": "urgent"})
    assert r.status_code == 201
    data = r.json()
    assert data["name"] == "urgent"
    assert "id" in data
    assert "created_at" in data and "updated_at" in data

    r = client.post("/tags/", json={"name": "review"})
    assert r.status_code == 201

    r = client.get("/tags/")
    assert r.status_code == 200
    tags = r.json()
    assert len(tags) >= 2


def test_get_tag(client):
    r = client.post("/tags/", json={"name": "bug"})
    tag_id = r.json()["id"]

    r = client.get(f"/tags/{tag_id}")
    assert r.status_code == 200
    assert r.json()["name"] == "bug"


def test_get_tag_not_found(client):
    r = client.get("/tags/9999")
    assert r.status_code == 404


def test_create_duplicate_tag(client):
    client.post("/tags/", json={"name": "duplicate"})
    r = client.post("/tags/", json={"name": "duplicate"})
    assert r.status_code == 409


def test_add_and_remove_tag_from_note(client):
    # Create a note and a tag
    note_r = client.post("/notes/", json={"title": "Tagged Note", "content": "content"})
    note_id = note_r.json()["id"]

    tag_r = client.post("/tags/", json={"name": "feature"})
    tag_id = tag_r.json()["id"]

    # Add tag to note
    r = client.post(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 200
    note_data = r.json()
    assert any(t["id"] == tag_id for t in note_data["tags"])

    # Verify tag appears when fetching the note
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    assert any(t["name"] == "feature" for t in r.json()["tags"])

    # Remove tag from note
    r = client.delete(f"/tags/{tag_id}/notes/{note_id}")
    assert r.status_code == 200
    assert all(t["id"] != tag_id for t in r.json()["tags"])


def test_add_tag_to_nonexistent_note(client):
    tag_r = client.post("/tags/", json={"name": "orphan"})
    tag_id = tag_r.json()["id"]
    r = client.post(f"/tags/{tag_id}/notes/9999")
    assert r.status_code == 404


def test_note_read_includes_tags_field(client):
    r = client.post("/notes/", json={"title": "No Tags", "content": "empty"})
    assert r.status_code == 201
    assert r.json()["tags"] == []
