# API Harvester

client-court covered the judgment calls: what to do with each status
code, how pagination works, why timeouts and retry limits matter,
which methods are safe to retry. This assignment puts that judgment
into working code. You will write five small CLIENT functions -- code
that CALLS an API, as opposed to row 58's Flask assignment, which
wrote the SERVER side. Every function takes a `fetch` parameter: a
callable you call as `fetch(path)`, which returns a `(status_code,
body)` tuple, exactly like a real HTTP client would give you after
parsing a response.

## Learning goals

- Follow PAGINATION correctly: loop through pages using a `next` link
  until there are no more, instead of stopping after the first page
- Implement a RETRY policy with an exact attempt count: retry only on
  a server error (status >= 500), never on a client error (4xx), and
  never more than a fixed number of extra attempts
- Handle a "not found" result (404) as a normal, expected outcome
  (`None`), not a crash
- Practice writing functions against an injected dependency (`fetch`)
  instead of a concrete library, so the same logic could later be
  pointed at a real HTTP client with no changes to the logic itself
- Read and apply type hints on a `Callable` parameter

## Examples at a glance: every function on one dataset

To make the five functions concrete, here is **one** small fake user
dataset -- 3 users, split across pages of 2 -- and what every function
returns for it. Read this table first; it is the whole assignment in
miniature.

```
users = [
    {"id": 1, "name": "ada", "active": True},
    {"id": 2, "name": "bo",  "active": False},
    {"id": 3, "name": "cy",  "active": True},
]
```

The fake `fetch` behind this dataset serves two kinds of path:
`/users/<id>` (one profile, or a 404 if the id does not exist), and
`/users?page=N` (a page of at most 2 items, with a `"next"` link to the
following page, or `None` once there is no more data). With a page
size of 2 and 3 users total, page 1 holds `ada` and `bo` (with
`"next": "/users?page=2"`), and page 2 holds just `cy` (with
`"next": None`).

| Call | Returns | Why |
|------|---------|-----|
| `get_user(fetch, 1)` | `{"id": 1, "name": "ada", "active": True}` | user `1` exists, so the profile dict comes back as-is |
| `get_user(fetch, 999)` | `None` | no user has id `999`, so `fetch` reports a 404, and `get_user` turns that into `None` -- not a crash |
| `list_all_users(fetch)` | `[{"id": 1, ...}, {"id": 2, ...}, {"id": 3, ...}]` | page 1 gives `ada` and `bo` plus `next = "/users?page=2"`; page 2 gives `cy` plus `next = None`, so the loop stops after exactly 2 fetches |
| `count_active(fetch)` | `2` | of the three users, `ada` and `cy` have `"active": True`; `bo` does not |
| `merge_profiles(fetch, [1, 999, 3])` | `{1: {"id": 1, ...}, 3: {"id": 3, ...}}` | id `1` and `3` exist and are included; id `999` is silently skipped because `get_user` returned `None` for it |
| `safe_get(fetch, "/users/1", retries=3)` where the first 2 calls return `(500, None)` and the 3rd returns `(200, {...})` | `{"id": 1, "name": "ada", "active": True}` | 2 server errors get retried, the 3rd attempt succeeds, so `safe_get` returns that body after exactly 3 total calls |
| `safe_get(fetch, "/users/1", retries=2)` where every call returns `(500, None)` | `None` | `retries=2` allows 2 EXTRA attempts beyond the first (3 total); all 3 come back `>= 500`, so every attempt is exhausted and the function gives up |
| `safe_get(fetch, "/users/999", retries=3)` where the call returns `(404, None)` | `None`, after exactly **1** call | a 4xx is never retried -- `safe_get` returns immediately instead of burning any of its `retries` budget |

## Worked example: watch `list_all_users` and `count_active` run, page by page

This is the pattern most students get wrong on the first try (stopping
after page 1), so here is every step spelled out, using the same
3-user dataset above with a page size of 2.

`list_all_users(fetch)`:

| Step | Path requested | Body returned | What happens |
|------|-----------------|---------------|---------------|
| 1 | `/users?page=1` | `{"items": [ada, bo], "next": "/users?page=2"}` | `ada` and `bo` are appended to the running list; `next` is NOT `None`, so the loop keeps going |
| 2 | `/users?page=2` | `{"items": [cy], "next": None}` | `cy` is appended; `next` IS `None`, so the loop stops here |
| end | -- | -- | the running list is `[ada, bo, cy]` -- every user across both pages, in order |

If the loop had stopped after step 1 (a common bug), it would have
silently returned only `[ada, bo]` and dropped `cy` -- no error, no
crash, just a wrong (too-short) answer. This is why pagination bugs are
dangerous: they do not look like bugs, they look like "a smaller than
expected but plausible-looking result."

`count_active(fetch)` reuses exactly the list above instead of
re-fetching anything itself: it walks `[ada, bo, cy]`, checks each
user's `"active"` key, and counts `True` for `ada` and `cy` but not
`bo` -- giving `2`.

## Task

Implement five functions in a file named `harvester.py`. Every
function's first parameter is `fetch`, with this type:

```python
Fetch = Callable[[str], tuple[int, dict[str, Any] | list[Any] | None]]
```

Calling `fetch(path)` returns `(status_code, body)`. `status_code` is
an int (`200`, `404`, `500`, ...). `body` is the already-parsed JSON
value (a dict or list), or `None` if there is nothing to parse. You
never construct a URL, open a socket, or parse raw JSON text yourself
-- `fetch` does all of that; your job is only the CLIENT LOGIC of what
to do with what it gives back.

**Why no `requests` or `httpx`?** Because the lesson here is client
logic -- what to do per status code, how to follow pagination, when to
retry -- not the mechanics of opening a real network connection. In a
real project, you would replace the fake `fetch` used for testing with
a thin wrapper around a real HTTP library, for example:

```python
import requests

def real_fetch(path: str) -> tuple[int, dict | list | None]:
    r = requests.get(f"https://api.example.com{path}", timeout=5)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, None
```

None of the five functions below would need to change to use it --
that is the whole point of writing them against an injected callable
instead of a hardcoded library.

### Functions to implement

| Function | Behavior |
|----------|----------|
| `get_user(fetch, user_id)` | `GET /users/<user_id>`. Return the parsed profile dict, or `None` on a 404.<br>*Examples:* `get_user(fetch, 1) == {"id": 1, "name": "ada", "active": True}` (found)<br>`get_user(fetch, 999) is None` (404 -- id does not exist)<br>`get_user(fetch, 0) is None` on a `fetch` where nothing has id `0` (absent, same as any other 404 -- there is nothing special about id `0`) |
| `list_all_users(fetch)` | Fetch every user by following pagination starting at `/users?page=1`. Each page's body looks like `{"items": [...], "next": "/users?page=N"}` or `{"items": [...], "next": None}`. Keep requesting `next` until it is `None`, collecting every item along the way.<br>*Examples:* on the 3-user, page-size-2 dataset above, `list_all_users(fetch)` makes 2 calls (`page=1` then `page=2`) and returns all 3 users in order<br>on an empty dataset (page 1's body is `{"items": [], "next": None}`), `list_all_users(fetch) == []` -- one call, empty list, not an error<br>on a dataset that fits entirely on page 1 (`"next": None` already on the first call), `list_all_users(fetch)` makes exactly 1 call, never a second |
| `count_active(fetch)` | Paginate through every user (reuse `list_all_users`) and count how many have `"active": True`.<br>*Examples:* on the 3-user dataset above (`ada` and `cy` active, `bo` not), `count_active(fetch) == 2`<br>on a dataset where no user is active, `count_active(fetch) == 0` -- not an error, just zero<br>on an empty dataset, `count_active(fetch) == 0` as well |
| `safe_get(fetch, path, retries)` | Call `fetch(path)`. If the status is `>= 500`, retry, up to `retries` EXTRA attempts beyond the first (so `retries=2` means at most 3 total calls). Never retry a 4xx -- return its body immediately. Return `None` if every attempt came back `>= 500`.<br>*Examples:* first call already returns `(200, body)` with `retries=3` -- `safe_get` returns `body` after exactly **1** call, no retries spent<br>first 2 calls return `(500, None)`, 3rd returns `(200, body)`, `retries=3` -- returns `body` after exactly **3** calls<br>every call returns `(500, None)`, `retries=2` -- makes exactly **3** total calls (1 + 2 extra), then returns `None`<br>first call returns `(404, None)`, `retries=3` -- returns `None` after exactly **1** call; a 4xx never gets retried, no matter how large `retries` is |
| `merge_profiles(fetch, ids)` | Call `get_user` for every id in `ids`. Return a dict mapping `id -> profile` for every id that was found, silently skipping any id that came back 404.<br>*Examples:* `merge_profiles(fetch, [1, 999, 3])` on the 3-user dataset above `== {1: {"id": 1, ...}, 3: {"id": 3, ...}}` -- note `999` is missing from the result entirely, not mapped to `None`<br>`merge_profiles(fetch, [])` returns `{}` -- an empty id list gives an empty dict, no calls made<br>`merge_profiles(fetch, [999])` where `999` does not exist returns `{}` -- every id 404'd, so nothing is added |

### A tiny fake `fetch` you can test with

```python
def make_fetch(users):
    def fetch(path):
        if path.startswith("/users/"):
            uid = int(path.removeprefix("/users/"))
            user = next((u for u in users if u["id"] == uid), None)
            return (404, None) if user is None else (200, user)
        page = int(path.split("page=")[-1]) if "page=" in path else 1
        chunk = users[(page - 1) * 2 : page * 2]
        nxt = f"/users?page={page + 1}" if page * 2 < len(users) else None
        return 200, {"items": chunk, "next": nxt}
    return fetch

users = [{"id": i, "name": f"user{i}", "active": i % 2 == 0} for i in range(1, 6)]
fetch = make_fetch(users)
print(fetch("/users/3"))          # (200, {'id': 3, ...})
print(fetch("/users/999"))        # (404, None)
```

## Files

| File | Purpose |
|------|---------|
| `harvester.py` | Write your implementation here |

## Compilation and Testing

Put your finished `harvester.py` in this assignment's directory
(next to `README.md`), then run:

```bash
SUBMISSION_DIR=. python -m pytest visible-tests/test_visible.py -v
```

`SUBMISSION_DIR` tells the test file where to import `harvester.py`
from. Without it, the test file raises `KeyError: 'SUBMISSION_DIR'`
before any test can run.

## Constraints

- Do not rename `harvester.py`, or rename any of the five functions.
- Type hints are required: every function's parameters and return type,
  matching the `Fetch` callable type given in the starter.
- Standard library only. Do not import `requests`, `httpx`, or
  `urllib` -- all client logic must go through the injected `fetch`
  callable.
- `safe_get` must never retry a 4xx status, and must make exactly
  `retries + 1` total attempts when every attempt keeps returning a
  `>= 500` status.
- `list_all_users` must follow `next` until it is `None`; it must not
  stop after the first page.
- **Type-annotation bonus (10 pts):** every function must annotate all of its parameters and its return type. The bonus is awarded only when every function is fully annotated; a separate, informational [ty](https://docs.astral.sh/ty/) check then flags any annotation on `harvester.py` that does not hold up.

## Grading

| Component                                    | Points |
|-----------------------------------------------|--------|
| Import/token constraints (gate)                | 5      |
| Visible correctness tests                      | 35     |
| Hidden correctness tests                       | 50     |
| Complete type annotations (bonus)              | 10     |
| **Total**                                      | **100** |

Hidden tests cover: pagination boundaries (empty, single-page,
multi-page, exact page-size boundary), exact retry-attempt counts
(instrumented fake that counts calls), confirming a 404 or 400 is
never retried, and `merge_profiles` with a mix of found and missing
ids.

## Submission

Submit your implementation as `harvester.py`. Do not rename it.

## Going further

- Add exponential backoff (an actual sleep, growing between attempts)
  to `safe_get`, and a test double that fakes time instead of really
  sleeping.
- Write a `real_fetch` wrapper around `requests` or `httpx` (outside
  the graded file) and point your five functions at a real public API
  that offers pagination. Do your functions work unchanged?
- Add a `get_user_or_raise` variant that raises a custom exception
  instead of returning `None` on a 404, and discuss which of the two
  contracts (return `None` vs. raise) fits this use case better.
