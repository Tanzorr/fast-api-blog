from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import UserModel
from security import password_hash


# T-1, I-1
def test_duplicate_email_returns_409(client: TestClient, new_user: dict) -> None:
    payload = {"email": new_user["email"], "password": "other-password"}
    response = client.post("/users", json=payload)
    assert response.status_code == 409


# T-2, I-2
def test_password_is_saved_as_hash(
    client: TestClient, db: Session, new_user: dict
) -> None:
    saved = db.get(UserModel, new_user["id"])
    assert saved.password != new_user["password"]
    assert password_hash.verify(new_user["password"], saved.password)


# T-3, I-3
def test_users_responses_never_contain_password(client: TestClient) -> None:
    payload = {"email": "bob@example.com", "password": "secret-123"}
    user_id = client.post("/users", json=payload).json()["id"]
    responses = [
        client.post("/users", json={"email": "eve@example.com", "password": "x"}),
        client.get("/users"),
        client.get(f"/users/{user_id}"),
        client.put(f"/users/{user_id}", json=payload),
    ]
    for response in responses:
        assert response.status_code in (200, 201)
        assert "password" not in response.text


# T-5
def test_unknown_user_id_returns_404(client: TestClient) -> None:
    payload = {"email": "bob@example.com", "password": "secret-123"}
    assert client.get("/users/999").status_code == 404
    assert client.put("/users/999", json=payload).status_code == 404
    assert client.delete("/users/999").status_code == 404


# T-6
def test_user_create_get_update_delete(client: TestClient) -> None:
    created = client.post("/users", json={"email": "bob@example.com", "password": "a"})
    assert created.status_code == 201
    user_id = created.json()["id"]

    got = client.get(f"/users/{user_id}")
    assert got.status_code == 200
    assert got.json()["email"] == "bob@example.com"

    updated = client.put(
        f"/users/{user_id}", json={"email": "rob@example.com", "password": "b"}
    )
    assert updated.status_code == 200
    assert updated.json()["email"] == "rob@example.com"

    deleted = client.delete(f"/users/{user_id}")
    assert deleted.status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404
