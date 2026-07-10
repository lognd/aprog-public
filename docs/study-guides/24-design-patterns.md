# Study Guide 24: Design Patterns

This module teaches design patterns as refactor destinations, not
vocabulary: first name the code smell that makes working code painful to
extend, then match requirements to the pattern (or to no pattern at all),
then implement Strategy, Observer, and Template Method as fixes for three
legacy messes -- all using non-owning base pointers, no dynamic memory.

## Know before you start

- Runtime polymorphism: abstract base classes, pure virtual methods,
  vtable dispatch through `Base*`/`Base&` [assumed: row 23 -- Polymorphism]
- Non-owning pointers and who keeps the pointee alive [assumed: row 22 --
  Inheritance]
- `std::vector` for listener/log storage [assumed: row 7 -- Standard
  Library Types]

## Taught here

Concept: code smells
- Know that a code smell is a pattern in working, correct code that is not
  a bug but signals that a future change will be harder or riskier than it
  should be -- and that smells typically grow from a sequence of
  individually reasonable decisions, not one bad one.
- Know the five named smells: shotgun surgery (one conceptual change
  requires scattered edits in many places right now), copy-paste
  divergence (two copies that have already drifted because a fix reached
  only one), rigid switch on type (a `switch` that must grow a case per
  new variant), boolean parameter creep (call sites like `doThing(true,
  false, true)` that are unreadable without the signature), and the god
  function (one function doing several unrelated jobs).
- Know the diagnostic questions: what must change if one new requirement
  arrives? Does that change land in one place or many? Is everything in
  this function about the same job?
- Know the shotgun-surgery vs. copy-paste-divergence distinction: the
  first is about the pain of one change needing many scattered edits now;
  the second is about copies that have already silently desynced.

Concept: matching requirements to patterns (and to none)
- Know each pattern's trigger phrase: an unknown, growing set of listeners
  reacting to one event (Observer); several fully interchangeable whole
  algorithms behind one stable interface at one call site (Strategy); a
  fixed sequence of steps where exactly one step varies (Template Method);
  a nontrivial, repeated decision about which concrete class to construct
  (Factory).
- Know YAGNI ("You Aren't Gonna Need It"): flexibility for a need that
  does not exist yet has a real cost today (more classes, more
  indirection) for a benefit that may never arrive -- when a scenario
  explicitly rules out variation, "no pattern" is the correct answer.
- Be able to distinguish "this pattern fits" from overengineering by
  checking whether the pattern's trigger is actually present in the
  requirement.

Concept: Strategy
- Know that Strategy turns an algorithm's variable step into a separate
  object: the algorithm delegates the varying decision (e.g. a comparison
  `before(a, b)`) to a passed-in strategy object, so a new mode is a new
  class, not a new copy of the loop.
- Be able to implement an abstract strategy with one pure-virtual method,
  several concrete strategies (including one with a tie-break rule), and a
  free function that delegates every comparison to the strategy and
  hardcodes no ordering of its own.
- Know Strategy fixes the shotgun-surgery smell of a switch over
  near-identical copied loop bodies.

Concept: Observer
- Know that Observer lets a subject broadcast state changes to a set of
  listeners that register themselves at runtime: the subject holds
  non-owning observer pointers and calls a virtual hook on each when its
  state changes, so adding a new reaction is a new observer subclass, not
  an edit to the subject.
- Be able to implement `attach` (register a non-owning pointer), `detach`
  (truly remove, harmless if never attached), and a notify method that
  calls every attached observer in attach order.
- Know Observer fixes the rigidity smell of a function that cannot gain or
  lose a reaction without being edited, recompiled, and entangling every
  reaction with every other.

Concept: Template Method
- Know that Template Method fixes an algorithm's outline in a base class:
  a non-virtual skeleton method calls protected virtual hooks in a fixed
  order, while shared steps (like a footer) are defined exactly once in
  the base so variants can never desync.
- Know the "Hollywood principle" framing: don't call us, we'll call you --
  the base class calls the subclass's hooks, not the reverse.
- Know Template Method fixes the copy-paste-divergence smell of duplicated
  procedures whose shared parts (like a once-misspelled footer) drift
  apart.
- Be able to implement a base with a non-virtual `generate()` composing
  `header() + body() + footer()`, pure-virtual header/body hooks, and a
  shared non-virtual footer, matching required output byte for byte.

## Study checklist

- [ ] Name the five code smells and give a one-line description of each.
- [ ] Given a requirement, name the pattern whose trigger it matches -- or
      say "none needed" and justify it with YAGNI.
- [ ] Explain how Strategy removes the need to copy a loop body per mode.
- [ ] Explain why Observer's subject never changes when a new reaction is
      added.
- [ ] Explain how defining the footer once in a Template Method base fixes
      the divergence bug.

## Practiced in

`smell-hunt`, `pattern-matcher`, `pattern-toolkit`
