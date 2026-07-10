# Activity: Client Court

http-anatomy taught you what a request and response look like on the
wire. This activity is about the judgment calls a CLIENT (the code
calling an API, not the server serving it) has to make once real
responses start coming back: what to do with a success, what to do
with an absent resource, what to do when you are being rate limited,
what to do when the server itself is broken, where a secret belongs,
why large results come back a page at a time, why every network call
needs a deadline, what to do with a response that will not parse, and
which requests are safe to simply try again. None of these are code
you write in this activity -- they are the decisions you will make
constantly once you do write that code, in the assignment that
follows.

## Concepts covered

- What to do with each class of status code: 200 (use it), 404
  (handle absence), 429 (back off), 5xx (retry with a limit, or give
  up)
- RATE LIMITING: what it is and why a 429 means "slow down," not
  "broken" or "banned"
- Where an API key belongs (a header, not a query string) and why
  query strings are risky for secrets
- PAGINATION: what it is, why APIs page results, and the difference
  between page-number and cursor-based paging
- Why every network call needs a TIMEOUT, and why a hung call is
  worse than a failed one
- Handling a response body that fails to parse as JSON
- Which HTTP methods are safe to retry (idempotent ones) and which are
  not (POST can double-create)

## How it works

The launcher shows you ten scenarios and judgment calls, one at a
time -- no code. Type your answer. A correct answer shows a short
explanation and moves you on; a wrong answer shows an explanation of
the specific misconception behind that guess. Several questions build
directly on definitions from http-anatomy (idempotency, status code
classes) -- if a term feels unfamiliar, that activity is the place it
was first defined.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all ten questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask whose fault the status code is</summary>

4xx codes are the client's fault (the request itself needs to
change); 5xx codes are the server's fault (worth a limited retry). 429
is a special case of 4xx: the request was fine, you just sent it too
often.

</details>

<details>
<summary>Hint 2 -- ask what happens if the exact same request is sent twice</summary>

This is the same idempotency question from http-anatomy, applied to a
retry decision instead of a definition. If sending it twice would
double an effect (like creating two orders), it is not safe to retry
blindly.

</details>

<details>
<summary>Hint 3 -- think about where a full URL ends up written down</summary>

Access logs, browser history, and proxy logs all commonly record the
full URL a request was sent to, query string included -- but they do
not typically record header contents the same way.

</details>

## Going further

- Pick a real public API's documentation (many are free and require
  no signup) and find its rate-limiting policy. What headers does it
  use to tell you how many requests you have left?
- Look up "exponential backoff with jitter" and explain in your own
  words why the "jitter" part matters when many clients are retrying
  at once.
- Find a real API that uses cursor-based pagination in its
  documentation. What does its cursor value actually look like, and
  is it meant to be human-readable?
