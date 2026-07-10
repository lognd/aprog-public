# Activity: Who Handles the Wait

Four different things get called "concurrency" and constantly get confused
for each other: the event loop (`asyncio`), threading, the idea of
concurrency vs. parallelism itself, and hardware interrupts. This activity
is the flagship disambiguation document for all four -- twelve scenarios and
ASCII timelines, no code to run, where you classify which machine is at
work, name WHO decides when execution switches, and see exactly how the
four stack on top of each other. Read this before, during, or after
`concurrency-court` and `await-tracer` -- those two teach the tools; this
one teaches the vocabulary that keeps them from blurring together.

## Background

Here are the four terms, defined from scratch, before a single question.

An **event loop** is one worker (one thread, one CPU core) that juggles
many tasks by switching between them at points the running task's own code
chose to pause at -- in Python, an `await` statement. Nothing outside that
task's code decides when the switch happens; the task itself says "I am
about to wait on something, feel free to run someone else." This is called
**cooperative scheduling**: the loop only ever switches because the
running code cooperated by voluntarily yielding.

**Threading** means multiple separate OS-level worker threads exist, and
the operating system's own scheduler decides when to stop one and start
another -- at essentially any instruction, whether the running thread
"agreed" to it or not. This is called **preemptive scheduling**: the
switch can happen at a point the running code never marked, chosen by an
authority outside that code entirely.

**Concurrency** and **parallelism** are two different axes, not synonyms.
Concurrency is a *structural* property: how many tasks are in progress,
overlapping, at once -- it needs no particular number of CPU cores; one
core running an event loop already has real concurrency. Parallelism is
about *simultaneous execution*: more than one instruction from more than
one task genuinely running at the exact same instant, which is only
physically possible with more than one CPU core (or execution unit).

A **hardware interrupt** is an electrical signal from a physical device
(a keyboard, a network card, a timer chip) that forces the CPU to
suspend whatever it is doing -- mid-instruction, with zero cooperation
from the interrupted code -- jump to a small handler routine, and later
resume exactly where it left off. No loop, no thread, and no notion of "a
task" is required for an interrupt to happen; it is the most primitive of
the four mechanisms, and (as this activity shows) the other three are all
built on top of it somewhere.

### A four-column comparison

| | how many workers | who decides when it switches | can one blocked call stall the others? | needs multiple cores? |
|---|---|---|---|---|
| Event loop | one | the running task's own code, at `await` (cooperative) | yes -- a blocking call with no `await` freezes every task sharing that one thread | no |
| Threading | many | the OS scheduler, preemptively, without asking | no -- a blocking call stalls only that one thread; the others keep running | no |
| Hardware interrupt | n/a (not a scheduling model) | the hardware, asynchronously, with no cooperation asked | n/a -- there is no "other task" concept at this layer | no |
| Parallelism (as an axis) | many, genuinely simultaneous | whatever scheduling model is in use, PLUS multiple cores | depends on the scheduling model layered on top | yes |

### The layering that untangles the confusion

Two facts, drawn as one diagram, explain why these four ideas keep
tangling together: they are not four unrelated topics, they are four
different LAYERS built on top of each other.

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

Thread preemption is **built on** timer interrupts: a hardware clock
ticks at a fixed interval, forces the CPU into the OS's scheduler code,
and only THEN does the scheduler decide whether to switch threads. The
interrupt is what gives the scheduler its recurring opportunity to act;
the scheduling decision itself is a separate layer on top.

GUI and network "events" **originate** as hardware interrupts too -- a
mouse controller or network card signals the OS the same way a keyboard
does. The OS absorbs that raw interrupt (your code never touches it; only
the kernel has the privilege) and translates it into a structured,
queued item. Your event loop's code then picks that item up cooperatively,
at a point it chose to check (`pollEvent()`, `await queue.get()`) -- the
exact same mechanism as any other `await`. "Event-driven" at your code's
level is still cooperative scheduling; the raw interrupt happened one
layer further down, entirely inside the operating system.

### The same word, four machines: one keypress, four lenses

Trace a single keypress through all four:

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

- Classifying a scenario as an event loop, threading, a hardware
  interrupt, or plain sequential execution -- and telling them apart on
  sight
- WHO decides when execution switches: the running code itself
  (cooperative), the OS scheduler (preemptive), or the hardware
  (asynchronous interrupt)
- The verdict on an event loop: concurrent, not parallel -- one worker,
  many tasks in flight, never more than one truly executing
- Blocking-call blast radius: freezes everything sharing an event
  loop's one thread, but only its own thread inside threading
- Concurrency (structure: dealing with many at once) vs. parallelism
  (simultaneous execution: doing many at once, requires multiple cores)
- The layering: thread preemption is built on timer interrupts; GUI and
  network events originate as hardware interrupts absorbed by the OS
  and delivered to your event loop as queue items
- Polling (repeatedly checking) vs. interrupt-driven (passively
  notified) and the CPU cost difference between them

## How it works

The launcher shows you twelve questions, one at a time -- each with a
short scenario or an ASCII timeline diagram. Type your answer exactly.
A correct answer shows a short explanation and moves you on; a wrong
answer shows which specific confusion your guess represents (cooperative
vs. preemptive, interrupt vs. event loop, concurrency vs. parallelism,
polling vs. interrupt, sequential vs. concurrent) before you try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly answered all twelve questions and the launcher shows
you a passphrase.

## Hints

<details>
<summary>Hint 1 -- count the workers first</summary>

Before anything else, ask how many separate threads or processes are
actually in the picture. One worker switching at chosen points is an
event loop; more than one worker being switched by an outside authority
is threading; no worker/task concept at all, just a forced CPU jump, is
an interrupt.

</details>

<details>
<summary>Hint 2 -- "who decided this switch point" is the whole question</summary>

Cooperative means the running code itself chose the pause point.
Preemptive means an outside scheduler chose it, without asking.
Asynchronous (interrupt) means hardware forced it, with no scheduler or
running code involved in the decision at all.

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
  event loop is exactly the cooperative, single-thread machine this
  activity describes -- see snippet 5's interleaving proof in particular.
- SFML's game loop (see `sfml-anatomy`) is also a cooperative,
  single-threaded event loop -- not threading, and the events it reads
  from `pollEvent()` are, underneath, delivered the same way this
  activity's layering diagram describes. Compare the two loops directly.
- Write a tiny Python program with a `threading.Thread` doing a tight
  CPU-bound loop and a `print` statement right after starting it. Run it
  several times. Does the print always happen at the same point relative
  to the thread's progress? What does that tell you about who is really
  deciding the interleaving?
