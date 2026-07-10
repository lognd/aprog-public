# Study Guide 59: APIs

client-court builds the judgment calls a CLIENT (the code calling an
API) has to make once real responses start coming back -- what each
status-code class means for the caller, where a secret belongs, why
results get paged, why every call needs a timeout, how to handle a
body that will not parse, and which requests are safe to retry --
entirely without writing code. api-harvester then puts every one of
those judgment calls into working Python: five client functions
written against an injected `fetch` callable instead of a real HTTP
library, so the exact same logic could later point at `requests` or
`httpx` unchanged.

## Know before you start

- The four status-code classes and what each one means (200 success,
  201 created, 404 nothing at that path, 400 malformed request, 500
  server failure), and IDEMPOTENT meaning repeating an operation
  leaves server state unchanged, not that the response looks
  identical [assumed: row 58 -- Python Web Servers]
- The path/query-parameter/body distinction for where a piece of
  request data belongs [assumed: row 58 -- Python Web Servers]
- HTTP statelessness, and that GET/PUT/DELETE are idempotent while
  POST is not [assumed: row 58 -- Python Web Servers]
- Reading and writing `Callable` type annotations, since every
  api-harvester function takes a `Fetch = Callable[[str], tuple[int,
  ...]]` parameter [assumed: row 53 -- Python Generics & Typing]
- Reading and writing `dict`/`list`-shaped data, used for parsed JSON
  bodies and the `id -> profile` mapping `merge_profiles` returns
  [assumed: row 48 -- Python Data Structures]

## Taught here

Concept: status-code handling from the client's side
- Know a `200` response should be parsed and used immediately -- it
  is not a signal to retry or to treat as an error.
- Know a `404` is a normal, expected outcome a client should handle
  gracefully (for example, return `None`), not a crash and not
  something worth retrying, since the resource genuinely does not
  exist at that path.
- Know a `400` is the client's fault and retrying the identical
  request fails identically every time; a `500` is the server's fault
  and may be transient, so it is reasonable to retry a limited number
  of times with backoff before giving up.
- Be able to implement `safe_get(fetch, path, retries)`: retry only on
  a status `>= 500`, never on a 4xx (return its body immediately), and
  make exactly `retries + 1` total attempts before returning `None` if
  every attempt kept failing.

Concept: rate limiting
- Know RATE LIMITING is a deliberate server policy capping how many
  requests a client may make in a time window, not a bug and not a
  ban.
- Know the correct client response to a `429` is to back off -- wait,
  ideally for a growing amount of time, before retrying -- rather than
  retrying immediately at full speed.

Concept: where a secret belongs
- Know an API key belongs in a header (for example `Authorization`),
  not a query string, because full URLs -- query string included --
  routinely get written to access logs, browser history, and proxy
  logs, none of which are intended as secret storage.
- Know that encryption in transit protects a key while it travels, but
  does not protect where the URL ends up written down afterward.

Concept: pagination
- Know PAGINATION is splitting a large result set into smaller pages
  returned one request at a time, done because returning everything
  in one response would be slow and often wasteful.
- Know page-number pagination (`?page=2`) can skip or duplicate items
  if data changes between requests, while cursor-based pagination
  (`?cursor=...`) anchors to a specific marker and stays correct even
  as the underlying data changes.
- Be able to implement `list_all_users(fetch)`: follow a `{"items":
  [...], "next": "/users?page=N" | None}` response's `next` link,
  starting at `/users?page=1`, collecting every item until `next` is
  `None`, without stopping after the first page.
- Be able to reuse a pagination-following function to build another
  (`count_active(fetch)` counts `"active": True` items by reusing
  `list_all_users`), instead of re-implementing the page-following
  loop a second time.

Concept: timeouts
- Know a client should always set a TIMEOUT -- a hung call that never
  returns is strictly worse than a fast failure, because a failure can
  be detected and reacted to (retried, reported) while a hang gives
  the calling code no signal at all.

Concept: malformed responses
- Know a response body that fails to parse as JSON is a real, expected
  failure mode (a flaky connection, a server bug), not a programmer
  bug -- the correct handling is to catch it and report a clear
  failure, not crash with an unhandled exception and not silently
  return an empty result that looks identical to a legitimately empty
  success.

Concept: retry safety and idempotency
- Know which requests are safe to retry follows directly from
  idempotency: a timed-out GET is safe to retry because GET is
  idempotent, but a timed-out POST is not safe to retry blindly,
  because the server may have already processed the original request
  and a retry can create a second, duplicate resource.

Concept: writing client logic against an injected dependency
- Know writing functions against an injected callable (`fetch`,
  matching the type `Callable[[str], tuple[int, dict | list | None]]`)
  instead of a concrete HTTP library keeps the client logic (what to
  do per status code, how to follow pagination, when to retry)
  testable and swappable for a real library later with no change to
  the logic itself.
- Be able to implement `get_user(fetch, user_id)`: `GET /users/<id>`,
  returning the parsed profile on success or `None` on a 404.
- Be able to implement `merge_profiles(fetch, ids)`: call `get_user`
  for every id, returning a dict of `id -> profile` for every id that
  was found and silently skipping any id that came back 404.

## Study checklist

- [ ] Match 200/404/400/500/429 to the client action each one calls
      for, and explain why each action is correct.
- [ ] Define rate limiting and explain why immediate full-speed
      retries on a 429 make the situation worse.
- [ ] Explain why an API key belongs in a header instead of a query
      string, in terms of where URLs get logged.
- [ ] Define pagination and contrast page-number versus cursor-based
      paging.
- [ ] Explain why a hung network call with no timeout is worse than a
      fast failure.
- [ ] Explain the difference between a JSON parse failure, a
      legitimately empty success, and a crash, and why a client must
      not let any of the three look like one of the others.
- [ ] Explain, in terms of idempotency, why retrying a timed-out GET
      is safe but retrying a timed-out POST is not.
- [ ] Write a pagination-following loop that stops on `next: None`
      without an off-by-one or infinite-loop bug.
- [ ] Write a retry policy with an exact attempt count that never
      retries a 4xx.

## Practiced in

`client-court`, `api-harvester`
