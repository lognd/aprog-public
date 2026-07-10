# Activity: Await Tracer

`async`/`await` looks like ordinary sequential code, but it hands
control to an event loop -- a scheduler that decides which paused
coroutine to resume next -- at every `await`. This activity is seven
short Python programs that prove, by watching actual print output,
exactly how that scheduler behaves: when a coroutine's body actually
runs, what `asyncio.gather` really guarantees about ordering, and how
two coroutines genuinely interleave their progress on a single thread.
Every snippet uses either large timing gaps or `await asyncio.sleep(0)`
yield points, so every run is fully deterministic.

## Concepts covered

- `asyncio.run` as the entry point that actually drives a coroutine
- Calling a coroutine function without `await` returns a coroutine
  object; the body has not run yet
- Strict, sequential `await` ordering with no concurrency
- `asyncio.gather`: prints follow completion order; the returned list
  follows argument order, always
- Interleaving proof: two coroutines alternating progress across
  `await asyncio.sleep(0)` yield points
- A coroutine with no internal `await` still runs, but never yields the
  event loop partway through

## How it works

The launcher runs seven short Python programs on your own interpreter
and shows you each one's source code. Predict exactly what it prints
(entering each line separately when the output has more than one
line), then type your prediction. A correct guess shows a short
explanation and moves you on; a wrong guess shows the actual output and
an explanation of the misconception behind that guess.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all seven snippets and the
launcher shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- calling a coroutine function does nothing yet</summary>

Exactly like a generator function: `coro = some_coroutine_function()`
does not run a single line of the body. Only `await coro` (or
`asyncio.run(coro)`) actually drives it.

</details>

<details>
<summary>Hint 2 -- gather's prints follow completion time, its return list does not</summary>

`asyncio.gather(a(), b())`'s own side-effect prints happen in whichever
order the two coroutines actually finish. Its returned list is always
ordered to match the arguments you passed it -- `a`'s result first,
`b`'s result second -- no matter which one finished first.

</details>

<details>
<summary>Hint 3 -- await asyncio.sleep(0) is a pure yield point, not a real wait</summary>

It does not pause for any real time. It just hands control back to the
event loop so another ready task gets a turn, then resumes -- which is
exactly what makes the interleaving snippet fully deterministic.

</details>

## Going further

- Add a third `worker("C")` to the interleaving snippet's
  `asyncio.gather` call. Predict the full interleaved print order
  before running it.
- Replace one coroutine's `await asyncio.sleep(0.05)` with a real
  blocking `time.sleep(0.05)` (no `await`) inside `asyncio.gather`.
  What happens to the other coroutine's progress during that call?
- Look up `asyncio.wait` and `asyncio.as_completed`. How do their
  ordering guarantees differ from `asyncio.gather`'s argument-order
  return list?
