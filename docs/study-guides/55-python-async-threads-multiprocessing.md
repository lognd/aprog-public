# Study Guide 55: Python Async, Threads, Multiprocessing

This module teaches choosing among `asyncio`, `threading`, and
`multiprocessing` (or none of them) from first principles including the
GIL and race conditions, then proves `async`/`await`'s event-loop
scheduling behavior by tracing deterministic interleaved print output.

## Know before you start

- Generator pause/resume (calling a generator function runs no body code
  until pulled) as the direct analogue for calling a coroutine function
  [assumed: row 54 -- Python Generators]
- Shared mutable state and aliasing via shared object references [assumed:
  row 45 -- Intro to Python; row 47 -- Python Data Types]

## Taught here

Concept: choosing a concurrency tool
- Know **io-bound**: a workload whose runtime is dominated by WAITING on
  something outside the CPU -- disk, network, user input -- where a
  faster CPU does not help at all.
- Know **cpu-bound**: a workload whose runtime IS the computation
  itself, where only more or faster CPU cores help.
- Know `asyncio` fits many concurrent, I/O-bound waits (e.g. thousands of
  slow network requests) when everything involved is async-aware.
- Know `threading` fits a blocking, non-async-aware library called
  concurrently, still I/O-bound.
- Know `multiprocessing` fits CPU-heavy work that needs real
  multiple-core parallelism.
- Know some workloads need no concurrency tool at all -- recognize when
  the bottleneck is neither I/O wait nor CPU-bound parallelizable work.
- Be able to ask "what is the workload actually waiting on?" to choose
  correctly: network/disk wait -> asyncio/threading; CPU computation ->
  multiprocessing; no real bottleneck -> none.

Concept: the GIL and race conditions
- Know the GIL (Global Interpreter Lock) lets only one thread in a
  single Python process execute Python bytecode at a time.
- Know the GIL restricts THREADS, not processes -- separate processes
  each get their own interpreter and their own GIL, which is exactly why
  `multiprocessing`, not `threading`, provides real multi-core CPU
  parallelism.
- Know threads help I/O-bound work (waiting releases the GIL) but not
  CPU-bound work (the GIL serializes actual computation across threads
  in one process).
- Know a race condition is a bug arising from shared, mutable state
  accessed concurrently without coordination, where the outcome depends
  on unpredictable timing between threads.
- Know process memory isolation: separate processes do not share
  variables by default, unlike threads within one process, which do.

Concept: async/await mechanics
- Know `asyncio.run` is the entry point that actually drives a top-level
  coroutine.
- Know calling a coroutine function without `await` returns a paused
  coroutine object; the body has not run yet -- exactly like calling a
  generator function.
- Know a blocking call (no `await`, e.g. `time.sleep`) inside async code
  has no yield point for the event loop -- it runs as one uninterrupted
  chunk, freezing every other task scheduled on that same event loop.
- Know `await asyncio.sleep(0)` is a pure yield point (not a real time
  wait): it hands control back to the event loop so another ready task
  gets a turn, then resumes -- the mechanism that makes interleaving
  fully deterministic and testable.
- Know `asyncio.gather(a(), b())`'s own side-effect prints happen in
  whichever order the coroutines actually finish, but its RETURNED list
  is always ordered to match the arguments passed to it, regardless of
  completion order.
- Know a coroutine with no internal `await` still runs when awaited, but
  never yields the event loop partway through its own body.

Concept: three machines, unmistakably distinguished
- Event loop, threading, and concurrency-vs-parallelism are three
  DIFFERENT machines that get confused with each other constantly --
  know them well enough to classify any scenario on sight.
- Event loop: a loop that waits for events/ready tasks and dispatches
  them to handlers, switching where the running task's own code chose
  to pause (`await`) -- cooperative scheduling. Commonly implemented as
  one worker (`asyncio`, JavaScript, SFML's game loop), but the concept
  itself does not require single-threadedness -- it can be implemented
  multi-threaded/multi-core.
- Threading: many workers, switches happen wherever the OS scheduler
  decides, with no cooperation from the running thread -- preemptive
  scheduling.
- Blast radius of a blocking call: freezes every task sharing a
  single-threaded event loop's one thread; stalls only its own thread
  inside threading.
- Concurrency (structure: dealing with many things at once, needs no
  particular core count) vs. parallelism (simultaneous execution: doing
  many things at the same instant, requires multiple cores).
- Extra depth (see `who-handles-the-wait`'s README, not quizzed there):
  hardware interrupts -- the hardware forces the CPU to a handler
  asynchronously, with no thread and no loop required at all; thread
  preemption is built on hardware timer interrupts; GUI/network "events"
  originate as hardware interrupts, are absorbed by the OS, and are
  delivered to your event loop as already-packaged queue items -- your
  code never sees the raw interrupt itself.

## Study checklist

- [ ] Given a workload, choose asyncio, threading, multiprocessing, or
      none, and justify it.
- [ ] Define the GIL and explain why it restricts threads but not
      processes.
- [ ] Explain why threading helps I/O-bound but not CPU-bound work.
- [ ] Define a race condition with a concrete shared-state example.
- [ ] Predict the interleaved print order of two coroutines sharing
      await asyncio.sleep(0) yield points.
- [ ] Explain why asyncio.gather's prints and its returned list can have
      different orderings.

## Practiced in

`concurrency-court`, `await-tracer`, `who-handles-the-wait`
