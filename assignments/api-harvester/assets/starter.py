# api-harvester -- starter file.
#
# You are writing a small API CLIENT: functions that talk to a web API
# through an injected `fetch` callable instead of a real network
# connection. See README.md for the full contract and a runnable
# example fake `fetch` you can use to test your own code locally.
#
# Every function below receives `fetch` as its first argument:
#
#     fetch: Callable[[str], tuple[int, dict | list | None]]
#
# Calling fetch(path) returns a (status_code, body) tuple, exactly
# like a real HTTP client would give you after parsing the response --
# status_code is an int (200, 404, 500, ...) and body is the parsed
# JSON (a dict or list), or None when there is no body to parse.
#
# stdlib only. Do not import requests, httpx, or urllib -- the whole
# point of this assignment is the CLIENT LOGIC (what to do with each
# status code, how to follow pagination, when to retry), not the
# socket-level plumbing of actually making an HTTP connection. In
# real code you would swap the fake `fetch` here for a thin wrapper
# around requests.get(url).json() or httpx.get(url).json() -- but
# that wrapper is intentionally not part of this assignment.

# The signatures below are left UNANNOTATED on purpose: the type-annotation
# bonus asks you to add the hints yourself (the exact types are in the
# README). The `Fetch` type alias below is provided ready to annotate the
# first parameter of every function with.

from __future__ import annotations

from typing import Any, Callable  # noqa: F401 -- for you to annotate with

Fetch = Callable[[str], tuple[int, dict[str, Any] | list[Any] | None]]


def get_user(fetch, user_id):
    """Fetch one user by id from GET /users/<id>. Return None on a 404."""
    raise NotImplementedError


def list_all_users(fetch):
    """Fetch every user by following pagination starting at /users?page=1.

    Each page response looks like {"items": [...], "next": "/users?page=N"
    or None}. Keep requesting `next` until it is None, collecting every
    item along the way.
    """
    raise NotImplementedError


def count_active(fetch):
    """Paginate through every user and count how many have active=True."""
    raise NotImplementedError


def safe_get(fetch, path, retries):
    """Call fetch(path), retrying only on a >=500 status, at most `retries`
    extra attempts beyond the first. Never retry a 4xx. Return the parsed
    body on any non-5xx response, or None if every attempt returned 5xx.
    """
    raise NotImplementedError


def merge_profiles(fetch, ids):
    """Fetch each id in `ids` via GET /users/<id> and return a dict mapping
    id -> profile for every id that was found, silently skipping any id
    that comes back as a 404.
    """
    raise NotImplementedError
