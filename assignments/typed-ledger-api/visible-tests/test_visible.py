"""Visible tests for Typed Ledger API.

Run locally:
    python -m pytest visible-tests/test_visible.py -v
"""

import os
import sys

import pytest

sys.path.insert(0, os.environ["SUBMISSION_DIR"])

from app import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture()
def client():
    return TestClient(create_app())


def test_list_items_empty(client):
    resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_item_returns_201(client):
    resp = client.post("/items", json={"name": "pen", "qty": 3})
    assert resp.status_code == 201


def test_create_item_returns_created_object(client):
    resp = client.post("/items", json={"name": "pen", "qty": 3})
    body = resp.json()
    assert body["name"] == "pen"
    assert body["qty"] == 3
    assert "id" in body


def test_create_item_missing_name_returns_422(client):
    resp = client.post("/items", json={"qty": 3})
    assert resp.status_code == 422


def test_create_item_missing_qty_returns_422(client):
    resp = client.post("/items", json={"name": "pen"})
    assert resp.status_code == 422


def test_get_item_after_create_returns_200(client):
    created = client.post("/items", json={"name": "pen", "qty": 3}).json()
    resp = client.get(f"/items/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "pen"


def test_get_missing_item_returns_404(client):
    resp = client.get("/items/999")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "not found"}


def test_list_items_after_create_has_one_item(client):
    client.post("/items", json={"name": "pen", "qty": 3})
    resp = client.get("/items")
    assert len(resp.json()) == 1


def test_delete_item_returns_204(client):
    created = client.post("/items", json={"name": "pen", "qty": 3}).json()
    resp = client.delete(f"/items/{created['id']}")
    assert resp.status_code == 204


def test_delete_missing_item_returns_404(client):
    resp = client.delete("/items/999")
    assert resp.status_code == 404


def test_deleted_item_no_longer_gettable(client):
    created = client.post("/items", json={"name": "pen", "qty": 3}).json()
    client.delete(f"/items/{created['id']}")
    resp = client.get(f"/items/{created['id']}")
    assert resp.status_code == 404


def test_put_replaces_item_returns_200(client):
    created = client.post("/items", json={"name": "pen", "qty": 3}).json()
    resp = client.put(f"/items/{created['id']}", json={"name": "pencil", "qty": 5})
    assert resp.status_code == 200
    assert resp.json()["name"] == "pencil"
    assert resp.json()["qty"] == 5


def test_put_missing_item_returns_404(client):
    resp = client.put("/items/999", json={"name": "pencil", "qty": 5})
    assert resp.status_code == 404


def test_put_invalid_payload_returns_422(client):
    created = client.post("/items", json={"name": "pen", "qty": 3}).json()
    resp = client.put(f"/items/{created['id']}", json={"name": "pencil"})
    assert resp.status_code == 422
