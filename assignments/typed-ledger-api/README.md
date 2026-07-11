# Typed Ledger API

`tiny-ledger-api` built the exact same in-memory ledger on Flask: you
validated the JSON body of every request by hand (checking `isinstance`
one field at a time) and returned a `400` yourself whenever something
was wrong. That hand-validation was the whole point at the time -- it
forced you to see exactly what "validating a request" actually means,
one check at a time.

This assignment is the same domain -- the same items, the same five
routes, the same idea of an in-memory ledger -- rebuilt on FastAPI, a
framework built around Python's type hints. Instead of hand-checking
each field, you DECLARE the shape of an item once, as a typed class,
and the framework validates every incoming request body against that
declaration automatically, before your route function's body even
runs. This is the payoff of every activity and assignment this course
has spent on type hints: a type annotation stops being just
documentation and starts being something the framework actively uses.

## pydantic, in one paragraph

FastAPI is built on **pydantic**. A pydantic `BaseModel` is a class
whose fields are ordinary type-annotated attributes -- but unlike a
plain class or `dataclass`, pydantic actively validates data against
those annotations at the moment an instance is created from raw data
(like a JSON body), and raises a validation error if anything doesn't
match. FastAPI uses this directly: declare a route parameter's type as
a `BaseModel` subclass, and FastAPI parses the incoming JSON body into
that model automatically, rejecting the request with a `422` before
your function body runs at all if the body doesn't fit the shape you
declared. You are not calling any validation code yourself -- the
declaration IS the validation.

## Learning goals

- Declare a pydantic `BaseModel` and understand how FastAPI uses it to
  validate a request body automatically, with no hand-written checks
- Use FastAPI's `@app.get`/`@app.post`/`@app.put`/`@app.delete`
  decorators, matching each route to the HTTP method that fits its
  action (same mapping as `tiny-ledger-api`)
- Use the APP FACTORY pattern (`create_app()` returning a fresh
  `FastAPI` instance) for the same isolation reasons as the Flask
  assignment
- Use `response_model` to control exactly what shape a route sends
  back, so internal fields never leak into a client-facing response
- Recognize FastAPI's error body conventions, specifically the
  `{"detail": ...}` key it uses for both its own generated errors and
  your own raised `HTTPException`s -- a deliberate difference from the
  Flask assignment's `{"error": ...}` convention
- Test a FastAPI app with no real network traffic, using
  `fastapi.testclient.TestClient` to call routes directly and inspect
  the exact response

## Task

Implement a small FastAPI app in a file named `app.py`, structured
around a single factory function:

```python
def create_app() -> FastAPI:
```

Just like the Flask assignment, `create_app()` must build and return a
**fresh** `FastAPI` app on every call, with its own **private**
in-memory ledger (a plain Python dict of item id to item, plus
whatever you use to track the next id to assign) -- state created
inside `create_app()`, not at module scope, so two separate calls to
`create_app()` produce two apps with completely independent ledgers
and independent id sequences.

### The `Item` model

Declare a pydantic model for the data a client sends when creating or
replacing an item:

```python
class Item(BaseModel):
    name: str
    qty: int
```

You do **not** write any code that manually checks `isinstance(name,
str)` or similar -- declaring the type is the validation. If a client
sends a body where `qty` is missing, or is a string, or (like the
Flask assignment) is a `bool` (a `bool` is a subclass of `int` in
Python, but a `qty` that is actually `True`/`False` is not a valid
quantity -- pydantic's `int` validation already rejects `bool` values
for this reason), FastAPI generates a `422 Unprocessable Entity`
response **automatically**, before your route function's body runs at
all. **Do not hand-validate and return your own `400`** -- letting the
framework's own `422` happen on an invalid body is required, not
optional; a hidden test asserts the exact shape of FastAPI's
generated `422` error body.

An **item**, once stored, has an assigned `id` (an `int`, starting at
`1` and increasing by `1` for every item ever created in that app
instance's lifetime -- ids are never reused, even after the item they
belonged to is deleted), plus its `name` and `qty`.

### `response_model` and internal fields

Internally, store one extra field on each item beyond `id`, `name`,
and `qty` -- a `created_at` counter (a plain incrementing `int` is
fine; it does not need to be a real timestamp) recording the order an
item was created in. This internal field must **never** appear in any
response body. Declare a separate pydantic model for what a route
sends back, and set it as that route's `response_model`, so FastAPI
strips any field not declared on the response model automatically --
your route function can freely return the full internal dict (or an
object built from it); `response_model` is what guarantees the extra
field never reaches the client. Every route in the table below that
returns an item (`GET /items`, `GET /items/{id}`, `POST /items`,
`PUT /items/{id}`) must set a `response_model`.

## Examples at a glance

To make all five routes concrete at once, here is **one** running
ledger state and what every route produces for it. Start from a fresh
app (`client = TestClient(create_app())`), then run these calls **in
this order** -- each row's state depends on the rows above it:

1. `POST /items {"name": "pen", "qty": 3}` -> item `id=1` created.
2. `POST /items {"name": "mug", "qty": 1}` -> item `id=2` created.

Now, with items `1` (`pen`, qty `3`) and `2` (`mug`, qty `1`) both in
the ledger:

| Call | Status | Response body | Why |
|------|--------|----------------|-----|
| `GET /items` | `200` | `[{"id": 1, "name": "pen", "qty": 3}, {"id": 2, "name": "mug", "qty": 1}]` | lists both items, in creation order; note `created_at` never appears -- `response_model` strips it |
| `GET /items/1` | `200` | `{"id": 1, "name": "pen", "qty": 3}` | fetching an id that exists returns that one item |
| `GET /items/999` | `404` | `{"detail": "not found"}` | no item has id `999`; the key is `detail`, not `error` |
| `GET /items/abc` | `422` | `{"detail": [{"type": "int_parsing", "loc": ["path", "item_id"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "abc"}]}` | `item_id` is declared as `int` in the path; a non-numeric path segment fails FastAPI's own path-parameter validation before your function runs, the same way a bad body does |
| `POST /items {"name": "pen", "qty": 3}` | `201` | `{"id": 3, "name": "pen", "qty": 3}` | a third create gets id `3` -- ids keep counting up from however many items have ever existed, they never reuse a deleted id |
| `POST /items {"qty": 3}` | `422` | `{"detail": [{"type": "missing", "loc": ["body", "name"], "msg": "Field required", "input": {"qty": 3}}]}` | `name` is a required field on `Item` with no default; a missing field never reaches your route function at all |
| `POST /items {"name": "pen", "qty": "lots"}` | `422` | `{"detail": [{"type": "int_parsing", "loc": ["body", "qty"], "msg": "Input should be a valid integer, unable to parse string as an integer", "input": "lots"}]}` | `"lots"` cannot be parsed as an `int`; note `loc` is `["body", "qty"]`, pinpointing exactly which field failed |
| `DELETE /items/2` | `204` | (empty body) | deleting an existing item returns no content at all, not even `{}` |
| `DELETE /items/2` (again) | `404` | `{"detail": "not found"}` | item `2` no longer exists after the first delete -- deleting it twice is an error the second time |
| `PUT /items/1 {"name": "pencil", "qty": 5}` | `200` | `{"id": 1, "name": "pencil", "qty": 5}` | `PUT` fully replaces `name` and `qty`; the `id` stays `1` |
| `PUT /items/999 {"name": "x", "qty": 1}` | `404` | `{"detail": "not found"}` | no item has id `999` to replace |

Each `422` body's `"detail"` is always a **list** of error objects (one
per problem field), not a single string -- this is FastAPI's own
generated shape via pydantic, and it is the same shape whether the bad
data came from a JSON body or a path parameter. Your hand-written
`404`s use `"detail"` too, but as a plain string, matching the
convention FastAPI itself uses for `HTTPException`.

## Worked example: a full request sequence, step by step

This walks through one continuous sequence of requests against a
single fresh app, showing exactly how the ledger's state changes after
each call, and what triggers a validation error along the way. Assume
`client = TestClient(create_app())` right before step 1.

| Step | Request | Status | Response body | What changed |
|------|---------|--------|----------------|---------------|
| 1 | `GET /items` | `200` | `[]` | nothing yet -- a fresh app always starts with an empty ledger |
| 2 | `POST /items {"name": "pen", "qty": 3}` | `201` | `{"id": 1, "name": "pen", "qty": 3}` | item `1` is created; the next id counter is now at `2` |
| 3 | `GET /items/1` | `200` | `{"id": 1, "name": "pen", "qty": 3}` | reading back exactly what was just created; no `created_at` field leaks into the body |
| 4 | `POST /items {"name": "pen", "qty": true}` | `422` | `{"detail": [{"type": "value_error", "loc": ["body", "qty"], "msg": "Value error, qty must be an int, not a bool", "input": true, "ctx": {"error": {}}}]}` | **nothing** -- the ledger is untouched; `True`/`False` looks like a valid `int` in Python (`bool` is an `int` subclass) but is rejected as a quantity before your route body ever runs, and no item is created |
| 5 | `GET /items` | `200` | `[{"id": 1, "name": "pen", "qty": 3}]` | still just the one item from step 2 -- step 4's rejected request left no trace |
| 6 | `PUT /items/1 {"name": "pencil"}` | `422` | `{"detail": [{"type": "missing", "loc": ["body", "qty"], "msg": "Field required", "input": {"name": "pencil"}}]}` | **nothing** -- `PUT` requires a full `Item` body (both `name` and `qty`); a partial body is invalid, so the existing item `1` is left completely unchanged, not partially merged |
| 7 | `GET /items/1` | `200` | `{"id": 1, "name": "pen", "qty": 3}` | confirms step 6 changed nothing: still `pen`, qty `3`, exactly as after step 2 |
| 8 | `PUT /items/1 {"name": "pencil", "qty": 5}` | `200` | `{"id": 1, "name": "pencil", "qty": 5}` | this time the body is a complete, valid `Item`, so the replacement actually happens; the `id` stays `1` |
| 9 | `DELETE /items/1` | `204` | (empty body) | item `1` is gone from the ledger |
| 10 | `GET /items/1` | `404` | `{"detail": "not found"}` | confirms the delete took effect |
| 11 | `POST /items {"name": "clip", "qty": 10}` | `201` | `{"id": 2, "name": "clip", "qty": 10}` | the new item gets id `2`, **not** a reused `1` -- the id counter only ever goes up, regardless of deletes |

Step 4's exact `422` body is the important one to internalize: pydantic's
`"detail"` is always a list, each entry has `"type"`, `"loc"` (a path
telling you exactly which field, e.g. `["body", "qty"]`), `"msg"` (a
human-readable message), and `"input"` (the raw value that failed).
Custom validators (like the one rejecting `bool` for `qty`) add an
extra `"ctx"` key but otherwise produce the same shape as a built-in
type-mismatch error. This is FastAPI generating the response entirely
on its own -- no code in `app.py` builds this body by hand.

### Routes

| Method | Path | Behavior |
|--------|------|----------|
| `GET` | `/items` | List every item currently in the ledger. `200`, JSON array (possibly empty), each entry shaped by `response_model`. |
| `GET` | `/items/{item_id}` | Fetch one item. `200` with the item, or `404` with `{"detail": "not found"}`. |
| `POST` | `/items` | Create a new item from an `Item` body. `201` with the created object (including its assigned `id`), shaped by `response_model`. An invalid body produces FastAPI's own `422` -- do not hand-validate. |
| `DELETE` | `/items/{item_id}` | Delete an item. `204` with an empty body, or `404` with `{"detail": "not found"}`. |
| `PUT` | `/items/{item_id}` | Fully **replace** an existing item's `name` and `qty` from an `Item` body. `200` with the replaced object, shaped by `response_model`, or `404` with `{"detail": "not found"}` if the id does not exist. An invalid body produces FastAPI's own `422`. |

**Examples for `GET /items`:**
- **Example (empty ledger):** fresh app, nothing created yet ->
  `client.get("/items")` returns `200`, `[]` -- **an empty ledger is a
  `200` with an empty array, not a `404`**.
- **Example (after two creates):** `client.get("/items")` -> `200`,
  `[{"id": 1, ...}, {"id": 2, ...}]` -- every item currently stored, in
  the order they were created.
- **Example (after delete):** `client.get("/items")` -> `200`, `[]`
  again -- back to empty, same as the fresh-app case.

**Examples for `GET /items/{item_id}`:**
- **Example (existing id):** `client.get("/items/1")` -> `200`,
  `{"id": 1, "name": "pen", "qty": 3}`.
- **Error case (absent id):** `client.get("/items/999")` (never
  created, or already deleted) -> `404`, `{"detail": "not found"}`.
- **Tricky case (non-integer id in the URL):** `client.get("/items/abc")`
  -> **`422`, not `404`** -- `item_id` is declared as `int`, so a value
  that cannot even be parsed as an integer fails FastAPI's path
  validation before your route body runs at all, exactly like an
  invalid JSON body does.

**Examples for `POST /items`:**
- **Example (valid body):** `client.post("/items", json={"name": "pen", "qty": 3})`
  -> `201`, `{"id": 1, "name": "pen", "qty": 3}`.
- **Error case (missing field):** `client.post("/items", json={"qty": 3})`
  -> `422` with `"detail"` listing `{"loc": ["body", "name"], "type": "missing", ...}`
  -- **no item is created**.
- **Error case (wrong type):** `client.post("/items", json={"name": "pen", "qty": "lots"})`
  -> `422` with `"type": "int_parsing"` for the `qty` field -- a string
  that cannot be parsed as an int is rejected, not silently coerced.
- **Tricky case (bool for qty):** `client.post("/items", json={"name": "pen", "qty": True})`
  -> `422` -- `True`/`False` looks like an `int` in Python (`bool` is an
  `int` subclass) but **is not a valid quantity**, so it must be
  rejected rather than accepted as `1`/`0`.

**Examples for `DELETE /items/{item_id}`:**
- **Example (existing id):** `client.delete("/items/1")` -> `204`,
  empty body (not even `{}` -- **`204 No Content` means literally no
  body**).
- **Error case (absent id):** `client.delete("/items/999")` -> `404`,
  `{"detail": "not found"}`.
- **Tricky case (delete twice):** the first call on an id is `204`; the
  **second call on that same id is `404`**, because the item is already
  gone.

**Examples for `PUT /items/{item_id}`:**
- **Example (existing id, valid full body):** `client.put("/items/1", json={"name": "pencil", "qty": 5})`
  -> `200`, `{"id": 1, "name": "pencil", "qty": 5}` -- both fields
  replaced, `id` unchanged.
- **Error case (absent id):** `client.put("/items/999", json={"name": "x", "qty": 1})`
  -> `404`, `{"detail": "not found"}`.
- **Tricky case (partial body against an existing id):** `client.put("/items/1", json={"name": "pencil"})`
  (only `name`, missing `qty`) -> **`422`, not a partial merge** -- `PUT`
  requires a complete `Item` body, and the existing item is left
  completely unchanged when the body is invalid.

`PUT` replaces the item's entire content -- it does not merge in just
the fields present in the request body, same as the Flask assignment.
A `PUT` with an invalid body must leave the existing item completely
unchanged; FastAPI's own `422` handling already runs before your
function body does, so this falls out naturally as long as you do not
add extra state changes before validation would occur.

Note the `404` body's key: `{"detail": "not found"}`, **not**
`{"error": "not found"}`. FastAPI's convention (via `HTTPException`)
is `detail`, not `error` -- this is a deliberate, graded difference
from the Flask assignment, not a typo.

### Examples

```python
>>> from app import create_app
>>> from fastapi.testclient import TestClient
>>> client = TestClient(create_app())
>>> client.get("/items").json()
[]
>>> r = client.post("/items", json={"name": "pen", "qty": 3})
>>> r.status_code
201
>>> r.json()
{'id': 1, 'name': 'pen', 'qty': 3}
>>> client.get("/items/1").json()
{'id': 1, 'name': 'pen', 'qty': 3}
>>> client.get("/items/999").status_code
404
>>> client.post("/items", json={"name": "pen", "qty": "not a number"}).status_code
422
```

### `/docs` for free

Because every route's request and response shapes are declared as
typed pydantic models, FastAPI generates interactive API documentation
for you automatically, with zero extra code: run your app for real
(`fastapi dev app.py`, outside the test client) and visit `/docs` in a
browser to see every route, its expected request body, and its
response shape, along with a form to try requests directly from the
page. This is not graded -- it is a one-paragraph payoff for declaring
your types honestly, worth seeing at least once.

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
  return type, and on the `Item` model's fields.
- `fastapi` (and `pydantic`, which it depends on) is the only
  third-party import allowed, plus the standard library and `typing`.
  `flask` is not allowed.
- All server state (the ledger dict, the next-id counter) must live
  inside `create_app()`, not at module scope -- two calls to
  `create_app()` must produce two fully independent apps.
- Do not hand-validate request bodies and return your own `400` --
  let FastAPI's own `422` happen on invalid input. A hidden test
  checks the exact shape of a generated `422` error body.
- Every route returning an item must declare a `response_model` that
  excludes the internal `created_at` field. A hidden test asserts that
  field is absent from every response.
- Every `404` response body must be exactly `{"detail": "not found"}`.
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

Hidden tests cover: the exact shape of FastAPI's framework-generated
`422` error body on invalid input, `response_model` stripping the
internal `created_at` field from every response, id sequencing across
interleaved creates and deletes, `PUT` fully replacing (not merging)
an item's content, exact `404` `{"detail": "not found"}` bodies, and
factory isolation between two separate `create_app()` instances
(including their id sequences starting over independently).

## Submission

Submit your implementation as `app.py`. Do not rename it.

## Going further

- Add a `PATCH /items/{item_id}` route that updates only the fields
  present in the request body -- pydantic models support this via
  `model_fields_set` or an "all fields optional" variant of `Item`.
  How is the logic different from `PUT`'s full replacement?
- Compare this assignment's `app.py` line-by-line against
  `tiny-ledger-api`'s. How many lines of hand-written validation logic
  did declaring `Item` as a pydantic model eliminate?
- Run your app for real with `fastapi dev app.py` (outside the test
  client) and visit `/docs`. Try a request with a missing field
  directly from that page and read the `422` response it shows you.
