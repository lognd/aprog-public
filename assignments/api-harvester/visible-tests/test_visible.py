"""Visible tests for api-harvester.

Uses a small in-process fake `fetch` backed by a deterministic
in-memory user dataset -- no real network traffic, and no dependency
on the student's code beyond the five functions in harvester.py.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import parse_qs

sys.path.insert(0, os.environ["SUBMISSION_DIR"])

from harvester import (  # noqa: E402
    count_active,
    get_user,
    list_all_users,
    merge_profiles,
    safe_get,
)


class FakeAPI:
    """Deterministic fake backend: /users/<id> and paginated /users?page=N."""

    def __init__(self, users, page_size=10, fail_paths=None):
        self.users = users
        self.page_size = page_size
        self.call_log = []
        self._fail_state = dict(fail_paths or {})

    def fetch(self, path):
        self.call_log.append(path)
        if path in self._fail_state and self._fail_state[path] > 0:
            self._fail_state[path] -= 1
            return 500, None
        if path.startswith("/users/"):
            id_part = path[len("/users/"):]
            try:
                uid = int(id_part)
            except ValueError:
                return 400, {"error": "bad id"}
            user = next((u for u in self.users if u["id"] == uid), None)
            if user is None:
                return 404, None
            return 200, dict(user)
        if path.startswith("/users"):
            query = path.split("?", 1)[1] if "?" in path else ""
            params = parse_qs(query)
            page = int(params.get("page", ["1"])[0])
            start = (page - 1) * self.page_size
            end = start + self.page_size
            chunk = [dict(u) for u in self.users[start:end]]
            nxt = f"/users?page={page + 1}" if end < len(self.users) else None
            return 200, {"items": chunk, "next": nxt}
        return 404, None


def _users(n, active_every=2):
    return [
        {"id": i, "name": f"user{i}", "active": (i % active_every == 0)}
        for i in range(1, n + 1)
    ]


def test_get_user_found():
    api = FakeAPI(_users(5))
    assert get_user(api.fetch, 3) == {"id": 3, "name": "user3", "active": False}


def test_get_user_not_found_returns_none():
    api = FakeAPI(_users(5))
    assert get_user(api.fetch, 999) is None


def test_list_all_users_single_page():
    api = FakeAPI(_users(5), page_size=10)
    users = list_all_users(api.fetch)
    assert [u["id"] for u in users] == [1, 2, 3, 4, 5]


def test_list_all_users_multi_page():
    api = FakeAPI(_users(25), page_size=10)
    users = list_all_users(api.fetch)
    assert [u["id"] for u in users] == list(range(1, 26))


def test_list_all_users_empty():
    api = FakeAPI([], page_size=10)
    assert list_all_users(api.fetch) == []


def test_count_active_counts_correctly():
    api = FakeAPI(_users(10, active_every=2), page_size=10)
    assert count_active(api.fetch) == 5


def test_count_active_zero_when_none_active():
    api = FakeAPI(_users(5, active_every=1000), page_size=10)
    assert count_active(api.fetch) == 0


def test_safe_get_success_first_try():
    api = FakeAPI(_users(5))
    body = safe_get(api.fetch, "/users/1", retries=3)
    assert body == {"id": 1, "name": "user1", "active": False}
    assert len(api.call_log) == 1


def test_safe_get_retries_on_500_then_succeeds():
    api = FakeAPI(_users(5), fail_paths={"/users/1": 2})
    body = safe_get(api.fetch, "/users/1", retries=3)
    assert body == {"id": 1, "name": "user1", "active": False}
    assert len(api.call_log) == 3


def test_safe_get_no_retry_on_404():
    api = FakeAPI(_users(5))
    body = safe_get(api.fetch, "/users/999", retries=3)
    assert body is None
    assert len(api.call_log) == 1


def test_safe_get_exhausts_retries_returns_none():
    api = FakeAPI(_users(5), fail_paths={"/users/1": 10})
    body = safe_get(api.fetch, "/users/1", retries=2)
    assert body is None
    assert len(api.call_log) == 3


def test_merge_profiles_all_found():
    api = FakeAPI(_users(5))
    merged = merge_profiles(api.fetch, [1, 2, 3])
    assert set(merged.keys()) == {1, 2, 3}
    assert merged[1]["name"] == "user1"


def test_merge_profiles_skips_404():
    api = FakeAPI(_users(5))
    merged = merge_profiles(api.fetch, [1, 999, 3])
    assert set(merged.keys()) == {1, 3}
