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
- Use the APP FACTORY pattern (`create_app()` returning a fresh
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
