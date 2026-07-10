# Activity: Who Handles the Wait

Three different things get called "concurrency" and constantly get confused
for each other: the event loop (`asyncio`), threading, and the idea of
concurrency vs. parallelism itself. This activity is the flagship
disambiguation document for all three -- eight scenarios and ASCII
timelines, no code to run, where you classify which machine is at work,
name WHO decides when execution switches, and see exactly how concurrency
and parallelism are independent axes. Read this before, during, or after
`concurrency-court` and `await-tracer` -- those two teach the tools; this
one teaches the vocabulary that keeps them from blurring together.

Hardware interrupts show up too -- they underlie both thread preemption and
an event loop's I/O notifications -- but they are covered as extra depth in
this README, not quizzed. See the "Extra depth" section below.

## Background

Here are the three quizzed terms, defined from scratch, before a single
question.

An **event loop** is a loop that waits for events or ready tasks and
dispatches them to handlers, switching at points the running task's own
code chose to pause at -- in Python, an `await` statement -- rather than by
preemption. This is called **cooperative scheduling**: the loop only ever
switches because the running code cooperated by voluntarily yielding.
The event-loop CONCEPT does not itself require any particular number of
workers -- it is commonly implemented as one worker (one thread, one CPU
core) juggling many tasks (this is what `asyncio`, JavaScript, and SFML's
game loop all do), but nothing about "an event loop that dispatches at
yield points" rules out a multi-threaded or multi-core implementation.
This activity's scenarios and questions are explicit about which case is
in play; do not assume "event loop" means "single-threaded" as a matter
of definition.

**Threading** means multiple separate OS-level worker threads exist, and
the operating system's own scheduler decides when to stop one and start
another -- at essentially any instruction, whether the running thread
"agreed" to it or not. This is called **preemptive scheduling**: the
switch can happen at a point the running code never marked, chosen by an
authority outside that code entirely.

**Concurrency** and **parallelism** are two different axes, not synonyms.
Concurrency is a *structural* property: how many tasks are in progress,
overlapping, at once -- it needs no particular number of CPU cores; one
core running a single-threaded event loop already has real concurrency.
Parallelism is about *simultaneous execution*: more than one instruction
from more than one task genuinely running at the exact same instant,
which is only physically possible with more than one CPU core (or
execution unit).

### A three-column comparison

| | how many workers | who decides when it switches | can one blocked call stall the others? | needs multiple cores? |
|---|---|---|---|---|
| Event loop | commonly one; implementation-defined | the running task's own code, at `await` (cooperative) | yes, in the common single-threaded case -- a blocking call with no `await` freezes every task sharing that one thread | no |
| Threading | many | the OS scheduler, preemptively, without asking | no -- a blocking call stalls only that one thread; the others keep running | no |
| Parallelism (as an axis) | many, genuinely simultaneous | whatever scheduling model is in use, PLUS multiple cores | depends on the scheduling model layered on top | yes |

## Extra depth -- where interrupts fit (not quizzed)

This section is background reading, not part of the launcher's quiz. It
answers a question the three-machine comparison above leaves open: what
actually gives an OS scheduler or an event loop's queue its information
in the first place?

A **hardware interrupt** is an electrical signal from a physical device
(a keyboard, a network card, a timer chip) that forces the CPU to
suspend whatever it is doing -- mid-instruction, with zero cooperation
from the interrupted code -- jump to a small handler routine, and later
resume exactly where it left off. No loop, no thread, and no notion of "a
task" is required for an interrupt to happen; it is the most primitive
mechanism here, and both threading's preemption and an event loop's I/O
notifications are built on top of it somewhere underneath.

### The layering that untangles the confusion

Two facts, drawn as one diagram, explain how interrupts, threading, and
event loops relate: they are not unrelated topics, they are different
LAYERS built on top of each other.

```
                      hardware timer chip / keyboard / network card
                                      |
                                interrupt (asynchronous,
                                uninvited, no cooperation)
                                      |
                                      v
                      operating system's interrupt handler
                                     / \
                                    /   \
                                   /     \
                thread preemption          event/network notification
           (OS scheduler uses the         (OS packages the interrupt
            timer interrupt's regular      as a structured event and
            "tick" as its chance to        places it on a queue your
            decide: keep this thread       event loop can check --
            running, or switch?)           your code never sees the
                                            raw interrupt itself)
                                     \     /
                                      \   /
                                       v v
                          YOUR CODE: threads (preemptive)
                                  |          event loop (cooperative)
```

**Preemption is built on timer interrupts.** A hardware clock ticks at a
fixed interval, forces the CPU into the OS's scheduler code, and only
THEN does the scheduler decide whether to switch threads. The interrupt
is what gives the scheduler its recurring opportunity to act; the
scheduling decision itself is a separate layer on top. "The OS decides
when to switch threads" and "timer interrupts are involved" are two
different layers of the same mechanism, not competing explanations --
interrupt underneath, scheduling policy on top.

**Events originate as hardware interrupts too.** GUI and network "events"
originate as hardware interrupts just like a keypress does -- a mouse
controller or network card signals the OS the same way a keyboard does.
The OS absorbs that raw interrupt (your code never touches it; only the
kernel has the privilege to handle one directly) and translates it into
a structured, queued item. Your event loop's code then picks that item
up cooperatively, at a point it chose to check (`pollEvent()`,
`await queue.get()`) -- the exact same mechanism as any other `await`.
"Event-driven" at your code's level is still cooperative scheduling; the
raw interrupt happened one layer further down, entirely inside the
operating system, before your event loop ever got involved.

### Polling vs. interrupt

Two ways a program can learn "has something happened yet?":

- **Polling**: a loop that repeatedly checks a flag or condition, as fast
  as it can, even when nothing has changed. This wastes CPU cycles on
  every check, whether or not anything actually happened.
- **Interrupt-driven**: the program registers what it is interested in
  once, then does nothing further related to that check -- it is
  genuinely idle (or free to do other useful work) until something
  external actively notifies it. This costs essentially nothing while
  waiting and only spends CPU when there is genuinely something to
  handle.

This is precisely why real operating systems and event loops are built
on interrupts and notification queues rather than tight polling loops
for things like keyboard input, mouse movement, and network sockets.

### The same word, four lenses: one keypress

Trace a single keypress through all four ideas this README covers:

1. **As a hardware interrupt**: the keyboard controller signals the CPU.
   Whatever was executing is suspended mid-instruction, with zero
   cooperation, and the CPU jumps to a tiny handler. No loop, no thread,
   no task -- just a forced jump and a forced return.
2. **As a threading concern**: if your program has a dedicated input
   thread, the operating system's preemptive scheduler is what decides
   when that thread actually gets CPU time to notice the key was
   pressed -- it might be interrupted mid-check itself, by an unrelated
   timer tick, before it finishes handling the key.
3. **As an event-loop item**: the OS packages the keypress as a
   structured event and places it on a queue. Your event loop's code
   picks it up the next time it checks (`await` on the input queue,
   or `pollEvent()`) -- cooperative, at a point your code chose, using
   an item that started life as the interrupt from step 1.
4. **As a concurrency/parallelism question**: none of the above requires
   more than one CPU core. A single-core machine handles a keypress via
   interrupt, threading, and an event loop's queue just fine -- all
   concurrency, zero parallelism, the whole way through.

## Concepts covered

- Classifying a scenario as an event loop, threading, or plain sequential
  execution -- and telling them apart on sight
- WHO decides when execution switches: the running code itself
  (cooperative) or the OS scheduler (preemptive)
- The verdict on a single-threaded event loop: concurrent, not parallel
  -- one worker, many tasks in flight, never more than one truly
  executing
- Blocking-call blast radius: freezes everything sharing an event
  loop's one thread, but only its own thread inside threading
- Concurrency (structure: dealing with many at once) vs. parallelism
  (simultaneous execution: doing many at once, requires multiple cores)
- Extra depth (not quizzed, see README section above): hardware
  interrupts, the layering underneath thread preemption and event-loop
  I/O notifications, and polling vs. interrupt-driven design

## How it works

The launcher shows you eight questions, one at a time -- each with a
short scenario or an ASCII timeline diagram. Type your answer exactly.
A correct answer shows a short explanation and moves you on; a wrong
answer shows which specific confusion your guess represents (cooperative
vs. preemptive, concurrency vs. parallelism, sequential vs. concurrent)
before you try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all eight questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- count the workers first</summary>

Before anything else, ask how many separate threads or processes are
actually in the picture. One worker switching at chosen points is an
event loop; more than one worker being switched by an outside authority
is threading.

</details>

<details>
<summary>Hint 2 -- "who decided this switch point" is the whole question</summary>

Cooperative means the running code itself chose the pause point.
Preemptive means an outside scheduler chose it, without asking.

</details>

<details>
<summary>Hint 3 -- concurrency and parallelism are two different questions</summary>

"Are many tasks in progress at once?" is concurrency. "Are more than one
of them truly executing at the exact same instant?" is parallelism, and
it requires more than one CPU core. An event loop can answer yes to the
first and no to the second at the same time.

</details>

## Going further

- `await-tracer` proves, by observing real print output, that asyncio's
  event loop is exactly the cooperative, commonly-single-thread machine
  this activity describes -- see snippet 5's interleaving proof in
  particular.
- SFML's game loop (see `sfml-anatomy`) is also a cooperative event
  loop, in that case implemented on a single thread -- not threading,
  and the events it reads from `pollEvent()` are, underneath, delivered
  the same way this README's layering diagram describes. Compare the
  two loops directly.
- Write a tiny Python program with a `threading.Thread` doing a tight
  CPU-bound loop and a `print` statement right after starting it. Run it
  several times. Does the print always happen at the same point relative
  to the thread's progress? What does that tell you about who is really
  deciding the interleaving?
- Read about how a GUI toolkit or web server can implement an event
  loop with a worker pool behind it (multiple threads each pulling from
  the same ready-queue) rather than a single thread. What changes, and
  what stays the same, compared to the single-threaded case this
  activity quizzes?
