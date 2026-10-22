from fastapi.testclient import TestClient
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from models import post_likes
from tests.conftest import count_queries, login


def create_post(client: TestClient, title: str = "Title") -> int:
    response = client.post("/posts", json={"title": title, "content": "Text"})
    assert response.status_code == 201
    return response.json()["id"]


def count_likes_in_db(db: Session) -> int:
    return db.scalar(select(func.count()).select_from(post_likes))


# T-15
def test_like_post_returns_201_with_likes_count(
    client: TestClient, auth_headers: dict
) -> None:
    post_id = create_post(client)

    response = client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    assert response.status_code == 201
    assert response.json()["likes_count"] == 1


# T-15
def test_like_without_token_returns_401(client: TestClient) -> None:
    post_id = create_post(client)
    assert client.post(f"/posts/{post_id}/likes").status_code == 401


# T-15
def test_like_unknown_post_returns_404(client: TestClient, auth_headers: dict) -> None:
    assert client.post("/posts/999/likes", headers=auth_headers).status_code == 404


# T-16, I-6
def test_like_twice_returns_409(
    client: TestClient, auth_headers: dict, db: Session
) -> None:
    post_id = create_post(client)
    client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    response = client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    assert response.status_code == 409
    assert count_likes_in_db(db) == 1


# T-17
def test_unlike_returns_204_and_removes_the_like(
    client: TestClient, auth_headers: dict
) -> None:
    post_id = create_post(client)
    client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    response = client.delete(f"/posts/{post_id}/likes", headers=auth_headers)

    assert response.status_code == 204
    assert client.get("/posts").json()[0]["likes_count"] == 0


# T-17
def test_unlike_not_liked_post_returns_404(
    client: TestClient, auth_headers: dict
) -> None:
    post_id = create_post(client)
    response = client.delete(f"/posts/{post_id}/likes", headers=auth_headers)
    assert response.status_code == 404


# T-17
def test_unlike_without_token_returns_401(client: TestClient) -> None:
    post_id = create_post(client)
    assert client.delete(f"/posts/{post_id}/likes").status_code == 401


# T-18
def test_posts_list_shows_likes_count(
    client: TestClient, auth_headers: dict, other_user: dict
) -> None:
    liked_twice = create_post(client, "Liked twice")
    not_liked = create_post(client, "Not liked")
    other_headers = login(client, other_user["email"], other_user["password"])
    client.post(f"/posts/{liked_twice}/likes", headers=auth_headers)
    client.post(f"/posts/{liked_twice}/likes", headers=other_headers)

    counts = {post["id"]: post["likes_count"] for post in client.get("/posts").json()}

    assert counts == {liked_twice: 2, not_liked: 0}


# T-18
def test_posts_list_uses_the_same_number_of_queries_for_more_posts(
    client: TestClient, auth_headers: dict, test_engine: Engine
) -> None:
    first = create_post(client)
    client.post(f"/posts/{first}/likes", headers=auth_headers)
    with count_queries(test_engine) as one_post_queries:
        client.get("/posts")

    for _ in range(3):
        post_id = create_post(client)
        client.post(f"/posts/{post_id}/likes", headers=auth_headers)
    with count_queries(test_engine) as four_posts_queries:
        client.get("/posts")

    assert len(four_posts_queries) == len(one_post_queries)


# T-19
def test_my_likes_lists_the_posts_i_liked(
    client: TestClient, auth_headers: dict
) -> None:
    liked = create_post(client, "Liked")
    create_post(client, "Not liked")
    client.post(f"/posts/{liked}/likes", headers=auth_headers)

    response = client.get("/users/me/likes", headers=auth_headers)

    assert response.status_code == 200
    assert [post["id"] for post in response.json()] == [liked]


# T-19
def test_my_likes_without_token_returns_401(client: TestClient) -> None:
    assert client.get("/users/me/likes").status_code == 401


# T-20
def test_deleting_post_deletes_its_likes(
    client: TestClient, auth_headers: dict, db: Session
) -> None:
    post_id = create_post(client)
    client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    client.delete(f"/posts/{post_id}")

    assert count_likes_in_db(db) == 0


# T-20
def test_deleting_user_deletes_their_likes(
    client: TestClient, new_user: dict, auth_headers: dict, db: Session
) -> None:
    post_id = create_post(client)
    client.post(f"/posts/{post_id}/likes", headers=auth_headers)

    client.delete(f"/users/{new_user['id']}", headers=auth_headers)

    assert count_likes_in_db(db) == 0
    assert client.get("/posts").json()[0]["likes_count"] == 0
