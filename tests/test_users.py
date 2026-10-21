from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models import UserModel
from security import password_hash
from tests.conftest import login


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
def test_users_responses_never_contain_password(
    client: TestClient, new_user: dict, auth_headers: dict
) -> None:
    user_id = new_user["id"]
    payload = {"email": new_user["email"], "password": "new-secret"}
    responses = [
        client.post("/users", json={"email": "eve@example.com", "password": "x"}),
        client.get("/users"),
        client.get(f"/users/{user_id}"),
        client.get("/users/me", headers=auth_headers),
        client.put(f"/users/{user_id}", json=payload, headers=auth_headers),
    ]
    for response in responses:
        assert response.status_code in (200, 201)
        assert "password" not in response.text


# T-5
def test_unknown_user_id_returns_404(client: TestClient, auth_headers: dict) -> None:
    payload = {"email": "bob@example.com", "password": "secret-123"}
    assert client.get("/users/999").status_code == 404
    response = client.put("/users/999", json=payload, headers=auth_headers)
    assert response.status_code == 404
    assert client.delete("/users/999", headers=auth_headers).status_code == 404


# T-6
def test_user_create_get_update_delete(client: TestClient) -> None:
    created = client.post("/users", json={"email": "bob@example.com", "password": "a"})
    assert created.status_code == 201
    user_id = created.json()["id"]

    got = client.get(f"/users/{user_id}")
    assert got.status_code == 200
    assert got.json()["email"] == "bob@example.com"

    headers = login(client, "bob@example.com", "a")
    new_data = {"email": "rob@example.com", "password": "b"}
    updated = client.put(f"/users/{user_id}", json=new_data, headers=headers)
    assert updated.status_code == 200
    assert updated.json()["email"] == "rob@example.com"

    deleted = client.delete(f"/users/{user_id}", headers=headers)
    assert deleted.status_code == 204
    assert client.get(f"/users/{user_id}").status_code == 404
