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
| `get_user(fetch, user_id)` | `GET /users/<user_id>`. Return the parsed profile dict, or `None` on a 404. |
| `list_all_users(fetch)` | Fetch every user by following pagination starting at `/users?page=1`. Each page's body looks like `{"items": [...], "next": "/users?page=N"}` or `{"items": [...], "next": None}`. Keep requesting `next` until it is `None`, collecting every item along the way. |
| `count_active(fetch)` | Paginate through every user (reuse `list_all_users`) and count how many have `"active": True`. |
| `safe_get(fetch, path, retries)` | Call `fetch(path)`. If the status is `>= 500`, retry, up to `retries` EXTRA attempts beyond the first (so `retries=2` means at most 3 total calls). Never retry a 4xx -- return its body immediately. Return `None` if every attempt came back `>= 500`. |
| `merge_profiles(fetch, ids)` | Call `get_user` for every id in `ids`. Return a dict mapping `id -> profile` for every id that was found, silently skipping any id that came back 404. |

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

```bash
python -m pytest visible-tests/test_visible.py -v
```

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
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern
  Python type checker, run over `harvester.py`) earns a bonus.

## Grading

| Component                                    | Points |
|-----------------------------------------------|--------|
| Import/token constraints (gate)                | 5      |
| Visible correctness tests                      | 35     |
| Hidden correctness tests                       | 50     |
| Clean `ty` type-check (bonus)                  | 10     |
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
