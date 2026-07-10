# Study Guide 58: Python Web Servers

This module starts one floor lower than HTTP itself, with `osi-elevator`
building the very basic networking picture -- why layers, encapsulation
as nesting envelopes, and which layer HTTP/TCP/IP/Ethernet each live at
-- then builds the vocabulary and mental model of HTTP itself -- the
four parts of a request, the method-to-action mapping, status code
classes, idempotency, JSON, where a given piece of data belongs, and
statelessness -- before writing any server code. It then puts every
piece to work twice: first in `tiny-ledger-api`, a small Flask app
built with the app-factory pattern and a precise request/response
contract, and then again in `typed-ledger-api`, the same ledger domain
rebuilt on FastAPI, where a pydantic model replaces hand-written
validation.

## Know before you start

- Reading and satisfying a type-hinted function signature, since
  every route function requires parameter and return type hints
  [assumed: row 53 -- Python Generics & Typing]
- `bool` is a subclass of `int` in Python, directly relevant to
  rejecting a boolean `qty` value that would otherwise pass an
  `isinstance(x, int)` check [assumed: row 52 -- Python Types &
  Comprehensions]
- Decorator mechanics -- that `@app.get(...)` wraps the function
  defined immediately below it and decoration happens once, at
  import/definition time [assumed: row 49 -- Python Decorators]
- Reading and writing `dict`/`list`-shaped data, used for the
  in-memory ledger and JSON item objects [assumed: row 48 -- Python
  Data Structures]

## Taught here

Concept: OSI stack, very basics (`osi-elevator` comes before
`http-anatomy` -- it is the ground floor everything else in this
module stands on)
- Know networking is built in LAYERS specifically so each layer solves
  exactly one problem and trusts every layer below it to have already
  solved its own, instead of one piece of code solving everything at
  once.
- Know ENCAPSULATION means wrapping data in progressively more layers
  on the way out, like nesting envelopes -- an HTTP request is wrapped
  by TCP, then that is wrapped by IP, then that is wrapped by
  Ethernet/WiFi -- and UNWRAPPED in the exact reverse order on
  arrival.
- Know the practical five-layer model and which layer each thing
  lives at: HTTP (application), TCP (transport), IP (network),
  Ethernet/WiFi (link), the cable/radio signal itself (physical) --
  and honestly, that the traditional seven-layer count's session and
  presentation layers fold into application-layer tools in day-to-day
  web work rather than being treated as separate layers.
- Know what each identifier identifies: an IP address identifies
  which MACHINE, a port identifies which PROGRAM on that machine, and
  a MAC address identifies which network CARD on the local segment.
- Know DNS's one-sentence job: translating a human-readable name into
  the IP address to actually connect to.
- Know TCP's one-sentence job -- reliable, ordered delivery -- versus
  a "just send it" alternative that guarantees neither.
- Know a web developer's own code lives at the application layer and
  relies on every layer below it to have already done its job, which
  is why application code can treat the network as a simple pipe.

Concept: anatomy of an HTTP request and response
- Know every HTTP request has exactly four parts: the METHOD (the
  action requested), the PATH (which resource), HEADERS (metadata
  key-value pairs about the request), and the BODY (optional data
  the request carries).
- Know a STATUS CODE is a three-digit number belonging to the
  RESPONSE, not the request, summarizing what happened.
- Know the specific status codes 200 (general success), 201
  (success, and something new was created), 404 (nothing exists at
  the requested path), 400 (the request reached a valid path but its
  own content is malformed or incomplete), and 500 (the server
  failed unexpectedly on an otherwise-valid request).
- Know 404 is a location problem (path does not exist) while 400 is
  a content problem (path is valid, payload is not).

Concept: HTTP methods and idempotency
- Know GET is for reading a resource without modifying anything on
  the server; it is SAFE (never has side effects) as well as
  idempotent.
- Know POST is for creating a new resource where the server assigns
  the identifier, typically paired with a `201` response.
- Know PUT is for fully replacing an existing, already-identified
  resource's entire content with client-provided data; any field not
  included is gone, not left as it was.
- Know DELETE removes a resource so it no longer exists at that
  location.
- Know IDEMPOTENT means performing an operation once and performing
  it many times in a row leaves the server in the exact same
  resulting STATE either way -- this is about state, not about the
  response looking identical on every repeat (e.g. a second DELETE
  on an already-deleted resource commonly returns 404 instead of the
  first call's success code, yet both leave the resource gone).
- Know GET and PUT and DELETE are idempotent; POST is not, because
  repeating it creates a new resource (with a new server-assigned
  id) each time rather than reproducing the same end state.

Concept: JSON and where data belongs
- Know JSON (JavaScript Object Notation) is a lightweight, text-based
  data format (not a programming language) built from objects
  (key-value pairs), arrays, strings, numbers, booleans, and `null`,
  used as the standard format for HTTP request and response bodies.
- Know `Content-Type: application/json` is the header announcing that
  a body should be parsed as JSON.
- Know a resource's own identifier belongs in the PATH (required,
  hierarchical, the request is meaningless without it).
- Know an optional, named narrowing of an otherwise-complete request
  belongs in a QUERY PARAMETER (the `?key=value` part), not the path
  or body.
- Know data the client is sending to the server (new or replacement
  content) belongs in the BODY, and a GET request conventionally
  carries no body at all.

Concept: statelessness
- Know HTTP is STATELESS: by default the server remembers nothing
  about a client between one request and the next -- every request
  is handled as if it were the first.
- Know sessions (server-side record referenced by an id the client
  resends) and tokens (client-carried proof of identity resent with
  every request) exist specifically to compensate for HTTP having no
  built-in memory across requests, not because HTTP secretly
  remembers anything.

Concept: building a Flask app with the factory pattern
- Know the APP FACTORY pattern (`create_app()` returning a fresh
  `Flask` instance) keeps server state isolated per app instance
  instead of relying on module-level globals; state (the ledger dict,
  the next-id counter) is created inside `create_app()`'s own scope,
  so two separate calls produce two apps with fully independent
  state.
- Know Flask's `@app.get`/`@app.post`/`@app.put`/`@app.delete`
  decorators bind a route function to one HTTP method and path, and
  each route function requires type hints on its parameters and
  return type.
- Be able to validate a JSON request body's required fields and
  types before touching application state, returning `400` with a
  `{"error": "..."}` body on any missing field or wrong type
  (including rejecting a `bool` passed where an `int` quantity is
  expected, since `bool` is a subclass of `int`).
- Be able to implement PUT as a full replacement (not a merge):
  reject an invalid replacement body with `400` before mutating
  anything, leaving the existing item completely unchanged.
- Be able to assign ids starting at 1, incrementing for every item
  ever created in an app instance's lifetime, and never reusing an
  id after its item is deleted.
- Be able to test a Flask app with no real network traffic using
  `app.test_client()` to call routes directly and inspect the exact
  status code and JSON body.

Concept: FastAPI and typed validation
- Know a pydantic `BaseModel` is a class whose fields are ordinary
  type-annotated attributes that pydantic actively validates against
  when an instance is built from raw data (like a JSON body), unlike
  a plain class or `dataclass`, which does not check anything at
  runtime.
- Know declaring a route parameter's type as a `BaseModel` subclass is
  itself the validation -- FastAPI parses and validates the request
  body against that declared shape automatically, before the route
  function's body runs, and rejects an invalid body with its own
  `422` with no hand-written `isinstance` checks needed.
- Know FastAPI's error convention uses a `detail` key (both for its
  own generated errors and for a raised `HTTPException`), which is a
  deliberate difference from the Flask assignment's `error` key.
- Know `response_model` controls exactly what shape a route sends
  back, stripping any field not declared on it -- this is how an
  internal-only field (never meant for a client) is kept out of every
  response without needing to build a fresh dict by hand on every
  route.
- Be able to test a FastAPI app with no real network traffic using
  `fastapi.testclient.TestClient` to call routes directly and inspect
  the exact status code and JSON body.

## Study checklist

- [ ] Name the four parts of an HTTP request and explain what each
      one is for.
- [ ] Match GET/POST/PUT/DELETE to the read/create/replace/delete
      action each one fits, and justify each choice.
- [ ] Define idempotent precisely (in terms of server state, not
      response content) and state which of GET/POST/PUT is not
      idempotent, and why.
- [ ] Match 200/201/404/400/500 to the scenario each one signals.
- [ ] Given a piece of request data, decide whether it belongs in the
      path, a query parameter, or the body.
- [ ] Explain HTTP statelessness and why sessions/tokens exist.
- [ ] Explain why `create_app()` must build its state inside the
      function body rather than at module scope, and what breaks if
      it doesn't.
- [ ] Write a route that validates a JSON body's required fields and
      types (including rejecting `bool` for an `int` field) and
      returns the correct `400`/`404`/`200`/`201`/`204`.
- [ ] Explain why networking is layered, and name which layer HTTP,
      TCP, IP, and Ethernet/WiFi each live at.
- [ ] Trace the encapsulation order (TCP, then IP, then Ethernet/WiFi)
      on the way out and the unwrapping order in reverse on the way
      in.
- [ ] Explain what a pydantic `BaseModel` field declaration buys you
      that a plain class's type hints do not, and why declaring
      `Item(BaseModel)` is itself the validation in a FastAPI route.
- [ ] Explain what `response_model` does and why it is needed even
      when a route function could just build a "clean" dict by hand.

## Practiced in

`osi-elevator`, `http-anatomy`, `tiny-ledger-api`, `typed-ledger-api`
