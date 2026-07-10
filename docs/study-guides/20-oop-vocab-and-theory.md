# Study Guide 20: OOP Vocab & Theory (5 Pillars)

This module builds the vocabulary of object-oriented design before any
class syntax: the five pillars (abstraction, encapsulation, inheritance,
polymorphism, composition), and the is-a vs. has-a decision including the
classic traps where plain English suggests inheritance but the behavioral
contract forbids it.

## Know before you start

- The idea of a class bundling private data with the methods that guard it
  (paradigm-level exposure) [assumed: row 18 -- Programming Paradigms]

## Taught here

Concept: the five pillars
- Know that an object is a bundle of data plus the functions that operate
  on that data, and a class is the blueprint declaring an object's fields
  (data) and methods (attached functions).
- Know that abstraction means hiding complexity behind a simple, stable
  interface: the user's mental model stays tiny while the machinery stays
  the class author's problem -- it answers "what does the user need to
  think about?"
- Know that encapsulation means bundling data with the only methods allowed
  to touch it and blocking direct outside access (`private` in C++), so
  every change passes through validating methods and the data can never
  reach a nonsense state -- it answers "who may touch this data, and how?"
- Know the abstraction-vs-encapsulation tiebreaker: emphasis on simplifying
  what the user must THINK about (or on a swappable implementation) is
  abstraction; emphasis on what outside code is ALLOWED TO TOUCH is
  encapsulation.
- Know that inheritance declares a new (derived/child) class as an
  extension of an existing (base/parent) class, automatically reusing its
  fields and methods, and models an is-a relationship.
- Know that polymorphism ("many forms") means the same method call behaves
  differently depending on the actual object it lands on, chosen
  automatically at run time with no caller-side type checking -- one
  interface, many behaviors; inheritance is usually the enabling mechanism
  but the pillar is the effect.
- Know that composition means a class contains another object as a field
  and delegates work to it, modeling a has-a relationship (including
  has-many for collections), and that "favor composition over inheritance"
  is standard advice when the goal is only code reuse.

Concept: is-a vs has-a and the Liskov Substitution Principle
- Know that `class Car : public Vehicle` makes a public behavioral
  promise: a Car can be used anywhere a Vehicle is expected with zero
  surprises -- this is the Liskov Substitution Principle (LSP).
- Know that a contract is the set of assumptions callers are entitled to
  make about a class's methods, and that is-a in code is a claim about
  behavior, not vocabulary or biology.
- Know the Square/Rectangle trap: geometry says a square is a rectangle,
  but if `Rectangle` promises independent `setWidth`/`setHeight`, a
  `Square` forced to keep sides equal breaks that contract -- the honest
  design is often neither inheritance nor composition, but two separate
  classes sharing a small read-only interface.
- Know the Penguin/Bird trap: if the base `Bird` declares `fly()`,
  inheriting `Penguin` from it promises flight it cannot deliver; the fix
  is restructuring the hierarchy (a `FlyingBird` layer), not forcing the
  taxonomy into code.
- Know the implementation-inheritance trap: inheriting `Stack` from
  `Vector` just to reuse its storage publishes the whole vector interface
  (`insert`, indexing) and breaks the stack's guarantees -- the right
  relationship is has-a: a private `Vector` member exposing only
  push/pop/top. (This is exactly how `std::stack` is built, as a container
  adapter.)
- Be able to apply the substitution test mechanically: "can X be used
  everywhere a Y is expected, with zero surprises?" -- yes means is-a is
  defensible; "X needs a Y to do its job" means has-a; English saying is-a
  while a method breaks the promise means neither.

## Study checklist

- [ ] Name all five pillars and give a one-phrase definition of each.
- [ ] Given a scenario, apply the abstraction-vs-encapsulation tiebreaker.
- [ ] State the Liskov Substitution Principle in one sentence.
- [ ] Explain why Square inheriting from a mutable Rectangle is wrong even
      though geometry says otherwise.
- [ ] Explain why "I want its code" is not a reason to inherit and what to
      do instead.

## Practiced in

`pillar-identification`, `is-a-has-a`
