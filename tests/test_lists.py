from datetime import datetime

import httpx
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from models import PostModel, UserModel
from tests.conftest import count_queries, login


def add_post(
    db: Session,
    title: str = "Title",
    content: str = "Text",
    created_at: datetime | None = None,
) -> int:
    """Save a Post directly in the database, so the test can choose created_at."""
    post = PostModel(title=title, content=content)
    if created_at is not None:
        post.created_at = created_at
    db.add(post)
    db.commit()
    return post.id


def ids(response: httpx.Response) -> list[int]:
    assert response.status_code == 200
    return [row["id"] for row in response.json()]


# T-21
def test_posts_list_returns_the_first_20_by_default(
    client: TestClient, db: Session
) -> None:
    post_ids = [add_post(db) for _ in range(21)]
    assert ids(client.get("/posts")) == post_ids[:20]


# T-21
def test_users_list_returns_the_first_20_by_default(
    client: TestClient, db: Session
) -> None:
    # Saved directly: hashing 21 passwords through the API is slow.
    db.add_all(UserModel(email=f"u{i}@example.com", password="x") for i in range(21))
    db.commit()

    assert len(ids(client.get("/users"))) == 20


# T-21
@pytest.mark.parametrize("path", ["/posts", "/users"])
def test_limit_and_offset_return_pages_without_overlap(
    client: TestClient, db: Session, path: str
) -> None:
    for i in range(5):
        add_post(db)
        db.add(UserModel(email=f"u{i}@example.com", password="x"))
    db.commit()
    everything = ids(client.get(path))

    first_page = ids(client.get(path, params={"limit": 2}))
    second_page = ids(client.get(path, params={"limit": 2, "offset": 2}))
    after_the_end = ids(client.get(path, params={"offset": 100}))

    assert first_page + second_page == everything[:4]
    assert after_the_end == []


# T-21
@pytest.mark.parametrize("path", ["/posts", "/users"])
@pytest.mark.parametrize("params", [{"limit": 1}, {"limit": 100}, {"offset": 0}])
def test_limit_and_offset_at_the_edges_return_200(
    client: TestClient, path: str, params: dict
) -> None:
    assert client.get(path, params=params).status_code == 200


# T-21
@pytest.mark.parametrize("path", ["/posts", "/users"])
@pytest.mark.parametrize(
    "params",
    [{"limit": 0}, {"limit": 101}, {"limit": "abc"}, {"offset": -1}],
)
def test_wrong_limit_or_offset_returns_422(
    client: TestClient, path: str, params: dict
) -> None:
    assert client.get(path, params=params).status_code == 422


# T-22
def test_search_finds_the_word_in_title_or_content_in_any_case(
    client: TestClient, db: Session
) -> None:
    in_title = add_post(db, title="FastAPI tips", content="Short text")
    in_content = add_post(db, title="Notes", content="I like fastapi a lot")
    add_post(db, title="Cats", content="Dogs")

    assert ids(client.get("/posts", params={"search": "FASTapi"})) == [
        in_title,
        in_content,
    ]


# T-22
def test_search_treats_percent_as_a_plain_character(
    client: TestClient, db: Session
) -> None:
    add_post(db, title="Cats", content="Dogs")
    with_percent = add_post(db, title="Sale", content="50% off")

    assert ids(client.get("/posts", params={"search": "%"})) == [with_percent]


# T-23
def test_created_after_and_before_filter_by_created_at(
    client: TestClient, db: Session
) -> None:
    january = add_post(db, created_at=datetime(2026, 1, 1))
    february = add_post(db, created_at=datetime(2026, 2, 1))
    march = add_post(db, created_at=datetime(2026, 3, 1))

    after = {"created_after": "2026-01-15T00:00:00"}
    before = {"created_before": "2026-02-15T00:00:00"}

    assert ids(client.get("/posts", params=after)) == [february, march]
    assert ids(client.get("/posts", params=before)) == [january, february]
    assert ids(client.get("/posts", params=after | before)) == [february]


# T-23
def test_created_after_with_a_wrong_date_returns_422(client: TestClient) -> None:
    response = client.get("/posts", params={"created_after": "yesterday"})
    assert response.status_code == 422


# T-24
def test_min_likes_returns_posts_with_enough_likes(
    client: TestClient, db: Session, auth_headers: dict, other_user: dict
) -> None:
    two_likes = add_post(db)
    one_like = add_post(db)
    no_likes = add_post(db)
    other_headers = login(client, other_user["email"], other_user["password"])
    client.post(f"/posts/{two_likes}/likes", headers=auth_headers)
    client.post(f"/posts/{two_likes}/likes", headers=other_headers)
    client.post(f"/posts/{one_like}/likes", headers=auth_headers)

    assert ids(client.get("/posts", params={"min_likes": 0})) == [
        two_likes,
        one_like,
        no_likes,
    ]
    assert ids(client.get("/posts", params={"min_likes": 1})) == [two_likes, one_like]
    assert ids(client.get("/posts", params={"min_likes": 2})) == [two_likes]


# T-24
@pytest.mark.parametrize("min_likes", [-1, "many"])
def test_wrong_min_likes_returns_422(client: TestClient, min_likes: object) -> None:
    response = client.get("/posts", params={"min_likes": min_likes})
    assert response.status_code == 422


# T-25
def test_all_parameters_work_together_in_one_query(
    client: TestClient, db: Session, auth_headers: dict, test_engine: Engine
) -> None:
    old = add_post(db, title="Python", created_at=datetime(2025, 1, 1))
    add_post(db, title="Python", created_at=datetime(2026, 1, 1))  # not liked
    other_word = add_post(db, title="Go", created_at=datetime(2026, 1, 1))
    first = add_post(db, title="Python 1", created_at=datetime(2026, 1, 1))
    second = add_post(db, title="Python 2", created_at=datetime(2026, 1, 1))
    for post_id in [old, other_word, first, second]:
        client.post(f"/posts/{post_id}/likes", headers=auth_headers)
    filters = {"search": "python", "created_after": "2025-06-01", "min_likes": 1}
    page = {"limit": 1, "offset": 1}

    with count_queries(test_engine) as queries:
        response = client.get("/posts", params=filters | page)

    # old: too early; the second Post: no likes; other_word: no "python".
    assert ids(client.get("/posts", params=filters)) == [first, second]
    assert ids(response) == [second]
    assert len(queries) == 1
