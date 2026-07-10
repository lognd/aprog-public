# Activity: HTTP Anatomy

Before writing a single line of server code, you need the vocabulary
and the mental model of what actually crosses the wire when a browser
or client talks to a server. HTTP (HyperText Transfer Protocol) is the
shared rulebook both sides follow: every request has the same four
parts, every response carries a status code that falls into one of
five classes, and the protocol itself is deliberately STATELESS --
the server remembers nothing about you between one request and the
next, by design. This activity is ten no-code scenarios and
definitions covering exactly the vocabulary and rules you need before
building the Flask API in the assignment that follows it.

## Concepts covered

- The four parts of an HTTP request: method, path, headers, body
- Which HTTP method fits reading, creating, replacing, and deleting a
  resource (GET, POST, PUT, DELETE)
- Status code classes and five specific codes: 200, 201, 404, 400, 500
- IDEMPOTENCY: what it means, and which of GET/POST/PUT is not
  idempotent
- JSON (JavaScript Object Notation) defined from scratch
- Where a given piece of data belongs: path parameter, query
  parameter, or body
- Statelessness, and why sessions and tokens exist to compensate for
  it

## How it works

The launcher shows you eleven questions, one at a time -- scenarios,
definitions, or "which of these fits" prompts, no code. Type your
answer. A correct answer shows a short explanation and moves you on; a
wrong answer shows an explanation of the specific misconception behind
that guess. Read the explanations even on questions you get right the
first time -- several of them define a term precisely that a later
question depends on.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eleven questions and the launcher
shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- match the method to the verb in plain English</summary>

Read, create, replace, delete -- there is exactly one HTTP method for
each of those four actions. If you can name the plain-English action a
request is doing, you can name its method.

</details>

<details>
<summary>Hint 2 -- idempotent means "repeating it changes nothing further"</summary>

Ask: if this exact request were sent five times in a row, would the
server end up in the same state as if it had only been sent once?

</details>

<details>
<summary>Hint 3 -- path identifies, query parameters filter, body sends</summary>

If the request is meaningless without this piece of data, it belongs
in the path. If it is an optional narrowing of an otherwise-complete
request, it belongs in a query parameter. If the client is sending new
data to the server, it belongs in the body.

</details>

## Going further

- Open your browser's developer tools, go to the Network tab, and
  visit any web page. Find a real request and identify its method,
  path, headers, and (if present) body.
- Look up the full list of 4xx and 5xx status codes. Which ones have
  you seen in the wild, and what did they mean at the time?
- Read about PATCH, a fifth HTTP method not covered in this activity.
  How does it differ from PUT?
