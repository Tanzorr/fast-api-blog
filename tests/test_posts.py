import pytest
from fastapi.testclient import TestClient


# T-4, I-4
@pytest.mark.parametrize(
    "payload",
    [
        {"content": "Text"},
        {"title": "Title"},
        {},
    ],
)
def test_post_without_title_or_content_returns_422(
    client: TestClient, payload: dict
) -> None:
    assert client.post("/posts", json=payload).status_code == 422


# T-5
def test_unknown_post_id_returns_404(client: TestClient) -> None:
    payload = {"title": "Title", "content": "Text"}
    assert client.put("/posts/999", json=payload).status_code == 404
    assert client.delete("/posts/999").status_code == 404


# T-6
def test_post_create_list_update_delete(client: TestClient) -> None:
    created = client.post("/posts", json={"title": "First", "content": "Hello"})
    assert created.status_code == 201
    post_id = created.json()["id"]

    listed = client.get("/posts")
    assert listed.status_code == 200
    assert [post["id"] for post in listed.json()] == [post_id]

    updated = client.put(f"/posts/{post_id}", json={"title": "New", "content": "Bye"})
    assert updated.status_code == 200
    assert updated.json()["title"] == "New"

    deleted = client.delete(f"/posts/{post_id}")
    assert deleted.status_code == 204
    assert client.get("/posts").json() == []
