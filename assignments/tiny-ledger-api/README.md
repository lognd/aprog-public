# Tiny Ledger API

HTTP Anatomy laid out the vocabulary: methods, status codes,
idempotency, JSON, statelessness. This assignment builds a real,
small web server that puts every one of those pieces to work. You
will write a Flask app -- Flask is the framework this course uses for
a first server, over something like FastAPI, specifically because its
mental model is smaller: a Flask route is close to an ordinary Python
function with a decorator on it, with none of FastAPI's additional
machinery (Pydantic models, async endpoints, dependency injection) to
learn at the same time you are learning HTTP itself. The app manages
an in-memory "ledger" of items -- no database, no persistence, just a
dictionary that lives as long as the app process does -- behind five
routes that together cover all four HTTP methods this course has
introduced: GET, POST, PUT, DELETE.

## Learning goals

- Write Flask routes using the `@app.get`/`@app.post`/`@app.put`/
  `@app.delete` decorators, matching each route to the HTTP method
  that fits its action
- Use the **app factory** pattern (`create_app()` returning a fresh
  `Flask` instance) to keep server state isolated per app instance,
  instead of relying on fragile module-level globals
- Return exact status codes (200, 201, 204, 400, 404) and exact JSON
  error bodies matching a precise specification, not just "close
  enough"
- Practice request validation: rejecting a malformed JSON body with a
  `400` before ever touching application state
- Test a web server without any real network traffic, using Flask's
  `test_client()` to call routes directly and inspect the exact
  response

---

## Examples at a glance

To make all five routes concrete at once, here is **one** representative
sequence of state: an app that has just had one item created (`{"id": 1,
"name": "pen", "qty": 3}`) and nothing else. The table below shows what
every route produces against that exact state -- a call that reads state
does not change it, so the "state before" column is the same for every
row.

| Call | Status | Response body | Why |
|------|--------|----------------|-----|
| `GET /items` | `200` | `[{"id": 1, "name": "pen", "qty": 3}]` | lists every item currently in the ledger, as a JSON array |
| `GET /items/1` | `200` | `{"id": 1, "name": "pen", "qty": 3}` | id `1` exists |
| `GET /items/999` | `404` | `{"error": "not found"}` | no item has id `999` |
| `GET /items/abc` | `404` | (Flask's built-in HTML 404 page, not JSON) | the route is declared `/items/<int:item_id>`, so a path segment that is not an integer never matches this route at all -- Flask's own routing layer produces this 404, before any of your code runs |
| `POST /items` with `{"name": "pencil", "qty": 5}` | `201` | `{"id": 2, "name": "pencil", "qty": 5}` | a new item is created with the next id (`2`, since `1` is already taken) |
| `POST /items` with `{"qty": 5}` | `400` | `{"error": "missing or invalid 'name'"}` | `name` is absent |
| `POST /items` with `{"name": "pencil"}` | `400` | `{"error": "missing or invalid 'qty'"}` | `qty` is absent |
| `POST /items` with `{"name": "pencil", "qty": true}` | `400` | `{"error": "missing or invalid 'qty'"}` | `True`/`False` are technically `int` in Python but must be rejected as an invalid `qty` |
| `POST /items` with no body at all | `400` | `{"error": "invalid JSON body"}` | there is nothing to parse as JSON, so this fails before `name`/`qty` are even checked |
| `PUT /items/1` with `{"name": "pen", "qty": 4}` | `200` | `{"id": 1, "name": "pen", "qty": 4}` | id `1` exists, so its content is fully replaced |
| `PUT /items/1` with `{"name": "pen"}` | `400` | `{"error": "missing or invalid 'qty'"}` | `qty` missing from the replacement body -- item `1` is left completely unchanged (still `qty: 3`) |
| `PUT /items/999` with `{"name": "x", "qty": 1}` | `404` | `{"error": "not found"}` | no item has id `999`, checked before the body is even validated |
| `DELETE /items/1` | `204` | (empty body) | id `1` exists and is removed |
| `DELETE /items/999` | `404` | `{"error": "not found"}` | no item has id `999` |

## Worked example: create, read, break it, then delete

This walks through one continuous sequence of requests against a single
app instance from `create_app()`, showing exactly how the ledger's state
changes after each call. Every status code and JSON body below was
confirmed by running the reference solution directly.

1. `GET /items` (fresh app, nothing created yet)
   -> `200`, body `[]`
   Why: the ledger starts empty, so listing it returns an empty JSON
   array, not `404` or `null` -- "no items" is a valid, successful list.

2. `POST /items` with body `{"name": "pen", "qty": 3}`
   -> `201`, body `{"id": 1, "name": "pen", "qty": 3}`
   Why: `201 Created` (not `200`) signals a new resource came into
   existence; the server assigns `id: 1` since this is the first item
   ever created in this app instance.

3. `GET /items/1`
   -> `200`, body `{"id": 1, "name": "pen", "qty": 3}`
   Why: reading back the item just created returns exactly what was
   stored, including the server-assigned `id`.

4. `PUT /items/1` with body `{"name": "pencil"}` (missing `qty`)
   -> `400`, body `{"error": "missing or invalid 'qty'"}`
   Why: this is a validation error, not a "not found" -- item `1` exists,
   but the replacement body is invalid, so the request is rejected before
   any state changes.

5. `GET /items/1` (immediately after step 4)
   -> `200`, body `{"id": 1, "name": "pen", "qty": 3}`
   Why: this confirms the invalid `PUT` in step 4 left the item
   completely unchanged -- still `"name": "pen"`, still `"qty": 3`. A
   `PUT` that fails validation must never partially apply.

6. `DELETE /items/1`
   -> `204`, empty body
   Why: `204 No Content` is the correct success status for a delete --
   there is no resource left to describe, so the body is empty (not
   `{}` and not `null`).

7. `GET /items/1` (immediately after step 6)
   -> `404`, body `{"error": "not found"}`
   Why: the item is gone, so it is no longer gettable -- this is the same
   `404` shape used everywhere in the API, not a special "deleted" status.

8. `POST /items` with body `{"name": "paper", "qty": 10}`
   -> `201`, body `{"id": 2, "name": "paper", "qty": 10}`
   Why: this is the key "ids are never reused" behavior -- even though
   id `1` was deleted and the ledger is empty again, the next id assigned
   is `2`, not `1`. The id counter only ever increases, independent of
   deletions.

---

## Task

Implement a small Flask app in a file named `app.py`, structured
around a single factory function:

```python
def create_app() -> Flask:
```

`create_app()` must build and return a **fresh** `Flask` app on every
call, with its own **private** in-memory ledger (an ordinary Python
dict of item id to item, plus whatever you use to track the next id to
assign) -- state created inside `create_app()`, not at module scope, so
that two separate calls to `create_app()` produce two apps with
completely independent ledgers and independent id sequences. This is
required, not optional: it is how the grader gets a clean, isolated
app for every test.

An **item** is a JSON object `{"id": int, "name": str, "qty": int}`.
The `id` is assigned by the server, starting at `1` and increasing by
`1` for every item ever created in that app instance's lifetime --
**ids are never reused**, even after the item they belonged to is
deleted.

### Routes

| Method | Path | Behavior |
|--------|------|----------|
| `GET` | `/items` | List every item currently in the ledger. `200`, JSON array (possibly empty). |
| `GET` | `/items/<id>` | Fetch one item. `200` with the item, or `404` with `{"error": "not found"}`. |
| `POST` | `/items` | Create a new item from a JSON body `{"name": str, "qty": int}`. `201` with the created object (including its assigned `id`), or `400` with `{"error": "..."}` if `name` or `qty` is missing or the wrong type. |
| `DELETE` | `/items/<id>` | Delete an item. `204` with an empty body, or `404` with `{"error": "not found"}`. |
| `PUT` | `/items/<id>` | Fully **replace** an existing item's `name` and `qty`. `200` with the replaced object, `404` with `{"error": "not found"}` if the id does not exist, or `400` with `{"error": "..."}` if the new body is missing or the wrong type. |

*`GET /items` examples:* on a brand-new app, `GET /items` returns `200`
with body `[]` (an empty array, not `404` -- an empty ledger is still a
valid, successful list). After creating one item, it returns `200` with
`[{"id": 1, "name": "pen", "qty": 3}]`. Deleting that item afterward
returns the list to `[]` again -- items removed by `DELETE` disappear
from this list immediately.

*`GET /items/<id>` examples:* `GET /items/1` right after creating item
`1` returns `200` with `{"id": 1, "name": "pen", "qty": 3}`. `GET
/items/999` (an id that was never created) returns `404` with
`{"error": "not found"}`. `GET /items/abc` (a non-integer id) never
reaches your route handler at all: because the route is declared with
the `<int:item_id>` converter, Flask's own routing fails to match it and
returns its own built-in HTML `404` page, not your JSON error shape.

*`POST /items` examples:* `POST /items` with `{"name": "pen", "qty":
3}` on an empty ledger returns `201` with `{"id": 1, "name": "pen",
"qty": 3}`. `POST /items` with `{"qty": 3}` (missing `name`) returns
`400` with `{"error": "missing or invalid 'name'"}`. `POST /items` with
`{"name": "pen", "qty": true}` returns `400` with `{"error": "missing
or invalid 'qty'"}` -- `True`/`False` must be rejected as a `qty` even
though `bool` is technically a subclass of `int` in Python. `POST
/items` with no JSON body at all (or a non-JSON body) returns `400`
with `{"error": "invalid JSON body"}`, checked before `name`/`qty` are
even looked at.

*`DELETE /items/<id>` examples:* `DELETE /items/1` on an existing item
`1` returns `204` with an empty body (not `{}`, not `null` -- just
nothing). `DELETE /items/999` (never created, or already deleted)
returns `404` with `{"error": "not found"}`. Deleting an id does not
free it for reuse: after deleting item `1`, the next `POST /items` is
still assigned `id: 2`, never `id: 1` again.

*`PUT /items/<id>` examples:* `PUT /items/1` with `{"name": "pen",
"qty": 4}` on an existing item `1` returns `200` with `{"id": 1, "name":
"pen", "qty": 4}` -- the entire item is replaced, not merged. `PUT
/items/999` with a valid body returns `404` with `{"error": "not
found"}` -- checked before the body is even validated. `PUT /items/1`
with `{"name": "pencil"}` (missing `qty`) returns `400` with `{"error":
"missing or invalid 'qty'"}`, and afterward `GET /items/1` still shows
the OLD, unchanged item -- a failed `PUT` must never partially apply.

`PUT` replaces the item's entire content -- it does not merge in
just the fields present in the request body. A `PUT` with an invalid
body must leave the existing item completely unchanged (the `400`
happens before any state is modified).

A `qty` value of `True` or `False` must be rejected as invalid --
Python's `bool` is technically a subclass of `int`, but a quantity
that is actually a boolean is not a valid `qty`.

### Examples

```python
>>> from app import create_app
>>> client = create_app().test_client()
>>> client.get("/items").get_json()
[]
>>> r = client.post("/items", json={"name": "pen", "qty": 3})
>>> r.status_code
201
>>> r.get_json()
{'id': 1, 'name': 'pen', 'qty': 3}
>>> client.get("/items/1").get_json()
{'id': 1, 'name': 'pen', 'qty': 3}
>>> client.get("/items/999").status_code
404
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Write your implementation here |

## Compilation and Testing

```bash
python -m pytest visible-tests/test_visible.py -v
```

## Constraints

- Do not rename `app.py`, or rename/remove `create_app`.
- Type hints are required on every route function's parameters and
  return type.
- `flask` is the only third-party import allowed (plus the standard
  library and `typing`).
- All server state (the ledger dict, the next-id counter) must live
  inside `create_app()`, not at module scope -- two calls to
  `create_app()` must produce two fully independent apps.
- Error response bodies must match the spec exactly:
  `{"error": "not found"}` for every 404, and a `{"error": "..."}`
  shape (any nonempty message string) for every 400.
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern
  Python type checker, run over `app.py`) earns a bonus.

## Grading

| Component                              | Points |
|-----------------------------------------|--------|
| Import constraints (gate)               | 5      |
| Visible correctness tests               | 35     |
| Hidden correctness tests                | 50     |
| Clean `ty` type-check (bonus)           | 10     |
| **Total**                               | **100** |

Hidden tests cover: exact status codes and exact error bodies across
every route, id sequencing across interleaved creates and deletes,
`PUT` fully replacing (not merging) an item's content while leaving
an invalid `PUT` request's target item unchanged, and factory
isolation between two separate `create_app()` instances (including
their id sequences starting over independently).

## Submission

Submit your implementation as `app.py`. Do not rename it.

## Going further

- Add a `PATCH /items/<id>` route that updates only the fields present
  in the request body, leaving the rest unchanged -- how is its logic
  different from `PUT`'s full replacement?
- Add simple validation limits (`qty` must be non-negative, `name`
  must be non-empty after stripping whitespace) and return `400` with
  a specific message for each violation.
- Run your app for real with `flask run` (outside the test client) and
  hit it with `curl` from a separate terminal. What does a raw
  `curl -i` response look like, headers and all?
