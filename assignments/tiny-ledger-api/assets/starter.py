# tiny-ledger-api -- starter file.
#
# Implement a small Flask app: an in-memory "ledger" of items, built
# with the factory pattern (create_app()) so every test gets a fresh,
# isolated app with its own private ledger -- no state leaks between
# two app instances. See README.md for the exact spec of every route.
#
# flask is the only third-party import allowed. Type hints are
# required on every route function's parameters and return type.

from __future__ import annotations

from typing import Any

from flask import Flask, jsonify, request
from flask.typing import ResponseReturnValue


def create_app() -> Flask:
    """Build and return a fresh Flask app with its own private in-memory ledger."""
    app = Flask(__name__)

    # TODO: module-level-per-app state lives here (inside create_app,
    # not at module scope) -- a dict of item id -> item dict, and
    # whatever you need to track the next id to assign.

    @app.get("/items")
    def list_items() -> ResponseReturnValue:
        """List every item currently in the ledger."""
        raise NotImplementedError

    @app.get("/items/<int:item_id>")
    def get_item(item_id: int) -> ResponseReturnValue:
        """Fetch one item by id, or 404 if it does not exist."""
        raise NotImplementedError

    @app.post("/items")
    def create_item() -> ResponseReturnValue:
        """Create a new item from a JSON {"name": str, "qty": int} body."""
        raise NotImplementedError

    @app.delete("/items/<int:item_id>")
    def delete_item(item_id: int) -> ResponseReturnValue:
        """Delete an item by id: 204 (empty) on success, 404 if it does not exist."""
        raise NotImplementedError

    @app.put("/items/<int:item_id>")
    def replace_item(item_id: int) -> ResponseReturnValue:
        """Fully replace an existing item's content: 200, 404, or 400 on bad payload."""
        raise NotImplementedError

    return app
