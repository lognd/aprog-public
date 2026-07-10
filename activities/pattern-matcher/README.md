# Activity: Pattern Matcher

A design pattern is a reusable answer to a recurring structural problem --
not a rule you follow because it sounds professional. Every pattern also
has a cost: more classes, more indirection, more code a reader has to hold
in their head. This activity gives you concrete, real-world-shaped
requirements, with no code shown, and asks you to name which pattern (if
any) actually fits. Two of the scenarios are deliberate traps: the
requirement sounds like it needs a pattern, but a plain function or a
`vector` is genuinely the better answer.

## Concepts covered

- Recognizing Strategy, Observer, Template Method, and Factory from a
  plain-language requirement, without seeing any code
- YAGNI ("You Aren't Gonna Need It" -- the principle that you should not
  build flexibility for a need that does not exist yet, because that
  flexibility has a real cost today for a benefit that may never arrive)
- Telling apart "this pattern fits" from "this is overengineering"
- The specific trigger phrase each pattern responds to: an unknown,
  growing set of listeners (Observer); several interchangeable whole
  algorithms behind one interface (Strategy); a fixed sequence of steps
  with exactly one step that varies (Template Method); a nontrivial,
  repeated decision about which concrete class to construct (Factory)

## How it works

You are shown nine short scenarios describing a real requirement -- no
code, just a description of what the system needs to do. Each question
gives you an enumerated list of five options: strategy, observer, template
method, factory, or none needed. Type the one that fits, exactly as
written. A wrong answer explains specifically why that pattern's usual
trigger is not actually present in this scenario. A correct answer
explains what about the requirement matches the pattern's shape -- or, for
the "none needed" scenarios, why adding a pattern here would be pure
overengineering with no real problem behind it.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly matched all nine scenarios and the activity prints your
passphrase.

## Hints

- Observer's tell is a dynamic, possibly-unknown-in-advance SET of
  listeners reacting to one event, especially when new listeners
  (including code written by someone else, later) need to be added
  without touching the code that raises the event.
- Strategy's tell is ONE call site, ONE stable interface, with several
  FULLY interchangeable whole algorithms selected behind it -- not steps
  of a shared procedure, whole algorithms.
- Template Method's tell is a FIXED sequence of steps, shared by every
  case, where only one specific step in the middle actually varies.
- Factory's tell is a nontrivial decision about WHICH CONCRETE CLASS to
  construct, especially when that same decision logic is needed
  identically in more than one place.
- "None needed" is correct whenever the scenario explicitly rules out
  future variation (a fixed format, a single formula, one user, no
  anticipated change) -- read for that explicit signal before reaching
  for a pattern.
