from datetime import UTC, datetime, timedelta

import jwt
from fastapi.testclient import TestClient

from security import create_access_token, decode_access_token


def bearer(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def post_login(client: TestClient, email: str, password: str):
    return client.post("/auth/login", data={"username": email, "password": password})


# T-7
def test_login_returns_token_with_user_id(client: TestClient, new_user: dict) -> None:
    response = post_login(client, new_user["email"], new_user["password"])
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert decode_access_token(body["access_token"]) == new_user["id"]


# T-8
def test_login_with_wrong_password_returns_401(
    client: TestClient, new_user: dict
) -> None:
    response = post_login(client, new_user["email"], "wrong-password")
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}
    assert response.headers["WWW-Authenticate"] == "Bearer"


# T-9
def test_login_with_unknown_email_gives_same_401(
    client: TestClient, new_user: dict
) -> None:
    wrong_password = post_login(client, new_user["email"], "wrong-password")
    unknown_email = post_login(client, "nobody@example.com", new_user["password"])
    assert unknown_email.status_code == 401
    assert unknown_email.json() == wrong_password.json()


# T-10
def test_get_me_returns_logged_in_user(
    client: TestClient, new_user: dict, auth_headers: dict
) -> None:
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == new_user["id"]
    assert response.json()["email"] == new_user["email"]


def test_get_me_without_token_returns_401(client: TestClient) -> None:
    assert client.get("/users/me").status_code == 401


# T-11
def test_expired_token_returns_401(client: TestClient, new_user: dict) -> None:
    token = create_access_token(new_user["id"], expires_delta=timedelta(seconds=-1))
    assert client.get("/users/me", headers=bearer(token)).status_code == 401


# T-12
def test_token_with_wrong_secret_returns_401(
    client: TestClient, new_user: dict
) -> None:
    payload = {
        "sub": str(new_user["id"]),
        "exp": datetime.now(UTC) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, "x" * 32, algorithm="HS256")
    assert client.get("/users/me", headers=bearer(token)).status_code == 401


# T-13
def test_token_of_deleted_user_returns_401(
    client: TestClient, new_user: dict, auth_headers: dict
) -> None:
    deleted = client.delete(f"/users/{new_user['id']}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get("/users/me", headers=auth_headers).status_code == 401


# T-14 (AC-3)
def test_change_user_without_token_returns_401(
    client: TestClient, new_user: dict
) -> None:
    payload = {"email": "new@example.com", "password": "x"}
    assert client.put(f"/users/{new_user['id']}", json=payload).status_code == 401
    assert client.delete(f"/users/{new_user['id']}").status_code == 401


def test_change_other_user_returns_403(
    client: TestClient, auth_headers: dict, other_user: dict
) -> None:
    url = f"/users/{other_user['id']}"
    payload = {"email": "new@example.com", "password": "x"}
    assert client.put(url, json=payload, headers=auth_headers).status_code == 403
    assert client.delete(url, headers=auth_headers).status_code == 403
    assert client.get(url).json()["email"] == other_user["email"]


def test_change_own_user_works(
    client: TestClient, new_user: dict, auth_headers: dict
) -> None:
    url = f"/users/{new_user['id']}"
    payload = {"email": "new@example.com", "password": "x"}
    assert client.put(url, json=payload, headers=auth_headers).status_code == 200
    assert client.delete(url, headers=auth_headers).status_code == 204


# AC-6: the Authorize button in /docs uses this OAuth2 "password" flow.
def test_docs_authorize_button_points_to_login(client: TestClient) -> None:
    schemes = client.get("/openapi.json").json()["components"]["securitySchemes"]
    flow = schemes["OAuth2PasswordBearer"]["flows"]["password"]
    assert flow["tokenUrl"] == "/auth/login"
