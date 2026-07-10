# Activity: Concurrency Court

Python gives you three different tools for doing more than one thing at
once -- `asyncio`, `threading`, and `multiprocessing` -- and picking the
wrong one does not just cost performance, it can silently fail to help
at all. This activity is ten scenarios and definitions, no code: for
each one you argue for the right tool (or for using none of them), and
the launcher walks you through exactly why the other choices fall
short. Along the way you will define the GIL (Global Interpreter Lock,
the mechanism at the center of all of this) from scratch, and pin down
what a race condition actually is.

## Concepts covered

- Choosing `asyncio` for many concurrent, I/O-bound waits (thousands of
  slow network requests)
- Choosing `threading` for a blocking, non-async-aware library called
  concurrently
- Choosing `multiprocessing` for CPU-heavy work that needs real
  multiple-core parallelism
- Recognizing when no concurrency tool is needed at all
- The GIL (Global Interpreter Lock): what it restricts, and at what
  granularity
- Why threads help I/O-bound work but not CPU-bound work
- Race conditions on shared, mutable state between threads
- Process memory isolation: why separate processes do not share
  variables by default
- Why a blocking call inside `asyncio` code stalls the entire event
  loop, not just its own coroutine
- Hardware interrupts: what they are, and why they require neither a
  thread nor an event loop to exist at all
- The layering underneath threading: preemptive scheduling is built on
  hardware timer interrupts, not a separate mechanism
- The layering underneath asyncio's I/O events: network readiness
  originates as a hardware interrupt the OS absorbs and delivers to
  your event loop as a queued item, never as a raw interrupt

## How it works

The launcher shows you thirteen questions, one at a time -- workload
descriptions, or a request to define a term precisely. Type your
answer. A correct answer shows a short explanation and moves you on; a
wrong answer shows an explanation of the specific misconception behind
that guess. The explanations are the real content here -- read them
even when you get a question right the first time.

For the full four-way disambiguation of event loops, threading,
interrupts, and concurrency vs. parallelism -- since these four ideas
get confused with each other constantly -- see `who-handles-the-wait`.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all thirteen questions and the launcher
shows you a passphrase.

## Hints

<details>
<summary>Hint 1 -- ask what the workload is actually waiting on</summary>

If the bottleneck is waiting on the network or disk, you want
`asyncio` (when everything involved is async-aware) or `threading`
(when it is not). If the bottleneck is CPU computation, you want
`multiprocessing`. If there is no real bottleneck at all, you may not
need any of them.

</details>

<details>
<summary>Hint 2 -- the GIL (Global Interpreter Lock) restricts THREADS, not processes</summary>

The GIL lets only one thread in a single Python process execute Python
bytecode at a time. Separate processes each get their own interpreter
and their own GIL -- which is exactly why `multiprocessing`, not
`threading`, is the tool that gets you real multi-core CPU parallelism.

</details>

<details>
<summary>Hint 3 -- a blocking call has no yield point for the event loop</summary>

`asyncio`'s concurrency depends on every task voluntarily handing
control back to the event loop at `await` points. A plain, blocking
call (no `await`) never does that -- it runs as one uninterrupted chunk
on the loop's single thread, freezing every other task scheduled on it.

</details>

## Going further

- Time a CPU-heavy Python loop (say, summing squares up to ten million)
  run on a single thread, then split across four `threading.Thread`
  workers, then split across four `multiprocessing.Process` workers.
  Which one actually gets faster, and by roughly how much?
- Read about CPython's ongoing "free-threaded" (no-GIL) build effort.
  What would have to change about CPython's memory management for the
  GIL to be safely removed?
- Write a tiny `asyncio` program that accidentally calls
  `time.sleep(2)` (a blocking call) instead of
  `await asyncio.sleep(2)` inside one of several concurrently-scheduled
  tasks. Confirm for yourself that every other task's progress freezes
  for those two seconds.
