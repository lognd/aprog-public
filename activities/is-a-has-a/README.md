# Activity: Is-A vs Has-A

When you design object-oriented software, the single most consequential
decision you make about any two classes is how they relate. There are two
main options. **Inheritance** declares that one class is a kind of another
(a Car **is-a** Vehicle) and automatically reuses the other's fields and
methods. **Composition** declares that one class contains another as a part
(a Car **has-a** Engine) and delegates work to it. Choosing wrong is not a
style problem -- it produces code that lies about its own behavior and
breaks in ways that surprise everyone who uses it.

The trap is that plain English is a bad guide. "A square is a rectangle"
is true in geometry and can still be the wrong relationship to put in code.
This activity gives you pairs of classes and their intended behavior; you
answer `is-a`, `has-a`, or `neither` -- and the questions include the
classic traps that English sets for you.

---

## Background

### What inheritance actually promises

Writing `class Car : public Vehicle` in C++ does more than copy Vehicle's
members into Car. It makes a public promise: **a Car can be used anywhere a
Vehicle is expected, and nothing will go wrong.** Any function that takes a
Vehicle must work correctly when handed a Car, without knowing or caring
that it got one.

This promise has a name: the **Liskov Substitution Principle** (LSP, named
after computer scientist Barbara Liskov). It says a derived class must
honor every behavioral expectation -- every **contract** -- that the base
class establishes. A contract here just means the assumptions callers are
entitled to make: "calling `setWidth` does not change the height," "any
object with `fly()` can actually fly."

The crucial consequence: is-a in code is a claim about **behavior**, not
about vocabulary or biology. That is where the traps live.

### Trap 1: Square and Rectangle

Geometry says every square is a rectangle. So should `Square` inherit from
`Rectangle`? Suppose `Rectangle` has `setWidth(w)` and `setHeight(h)`, and
callers reasonably assume the two are independent -- setting the width does
not change the height. A `Square` must keep width and height equal, so its
`setWidth(5)` is forced to silently change the height too. Now every
function that was written against Rectangle's contract can break when
handed a Square. English said is-a; the mutable interface said no. The
honest design is often `neither`: two separate classes, perhaps both
implementing a small read-only interface (say, `area()` and `perimeter()`),
with no inheritance between the two concrete shapes.

### Trap 2: Penguin and Bird

Biology says a penguin is a bird. But if the `Bird` base class declares
`fly()`, then `Penguin : public Bird` promises that penguins fly. Every
caller holding a `Bird` reference is entitled to call `fly()` and expect
flight. Inheritance models behavioral contracts, not taxonomy (the
scientific classification of living things). The fix is to redesign the
hierarchy: keep `fly()` off the base `Bird`, and introduce a `FlyingBird`
subclass or interface that only the flying species derive from. As
designed -- with `fly()` on `Bird` -- the correct answer is `neither`.

### Trap 3: Stack and Vector (inheriting just to reuse code)

You are writing a `Stack` class (push, pop, top -- last in, first out) and
you already have a `Vector` class with `push_back`, `pop_back`, and
resizable storage. Tempting shortcut: inherit `Stack` from `Vector` and get
all that machinery for free. But inheritance publishes the whole base
interface: a `Stack` that is-a `Vector` lets callers `insert()` into the
middle and index any element -- operations that break the entire point of a
stack. Wanting to reuse an implementation is not a reason to inherit. The
right relationship is has-a: `Stack` holds a `Vector` as a private field,
uses it internally, and exposes only push/pop/top.

### When is-a is genuinely right

Inheritance is the correct tool when the derived class honors the full base
contract with no broken assumptions. `Dog : public Animal` where Animal
promises `eat()`, `sleep()`, `makeSound()` -- a dog does all three,
faithfully, everywhere an Animal is expected. `Employee : public Person` --
an employee has a name and a birth date and behaves as a person in every
context that only knows about persons. Small, read-only base interfaces are
the safest to inherit from, because there are fewer promises to break.

### When has-a is right

Composition is the correct tool whenever one object is built from, owns, or
uses another: a Car has-an Engine, a House has Rooms, a Team has a list of
Employees. Notice the last one: has-a covers collections too ("has-many").
A Team is never substitutable for a single Employee, so is-a is not even
close -- but the Team genuinely owns and works through its member objects.

A rule of thumb you can apply mechanically: ask **"can X be used everywhere
a Y is expected, with zero surprises?"** If yes, is-a is defensible. If
what you actually want is "X needs a Y to do its job," that is has-a. If
English says is-a but the methods disagree, believe the methods.

---

## Concepts covered

- Inheritance (is-a) vs composition (has-a), and how to choose
- The Liskov Substitution Principle: a derived class must honor the base
  class's behavioral contract
- Why English/taxonomy is-a can be wrong in code (Square/Rectangle,
  Penguin/Bird)
- The implementation-inheritance trap: inheriting to reuse code exposes an
  interface you do not want (Stack/Vector)
- has-many: composition over collections (Team/Employee)

---

## How it works

The launcher shows you nine questions. Each names two classes (or two
real-world nouns about to become classes), describes the intended behavior,
and asks how the relationship should be modeled. Every prompt ends with the
explicit option list:

```
Type exactly one of: is-a / has-a / neither
```

Type your answer exactly. Wrong answers get feedback explaining which
contract or containment detail you misjudged; correct answers unlock a full
explanation, including -- for the trap questions -- why the obvious English
reading fails. Answer all nine correctly and the launcher decrypts and
prints the passphrase.

Be warned: `neither` is a real answer, not a decoy. It is correct exactly
when English suggests is-a but the described interface makes the
substitution promise unkeepable.

---

## Getting started

```bash
python3 launch.py
```

For every pair, resist answering from the nouns alone. Look at the
described behavior -- which methods exist, what callers assume about
them -- and run the substitution test: could the first class stand in for
the second everywhere, with zero surprises?

---

## You will know you are done when...

The launcher prints `All correct.` followed by the passphrase between two
horizontal rules. Record the passphrase -- it is your proof of completion.

---

## Hints

<details>
<summary>Hint 1 -- the substitution test, step by step</summary>

Take every method the base class exposes and every assumption a caller
could reasonably make about it. Then ask: does the candidate derived class
keep all of those true? One broken assumption -- a setter that suddenly
couples two fields, a `fly()` that cannot fly -- means the is-a claim
fails, no matter what English says.

</details>

<details>
<summary>Hint 2 -- "I want its code" is not "I am one of it"</summary>

If your reason for inheriting is "the other class already implements the
storage/logic I need," stop. That is the implementation-inheritance trap.
Reuse through a private member field (has-a) gives you the same code
without publishing an interface you will regret. Inherit only when you
mean the substitution promise.

</details>

<details>
<summary>Hint 3 -- when neither is the answer</summary>

`neither` does not mean "no relationship exists in real life." It means
neither inheritance nor composition honestly models the relationship as
designed. The tell: English screams is-a, but a specific method in the
described interface (mutable setters, a capability the subtype lacks)
makes the substitution promise a lie -- and holding the other class as a
member part does not describe reality either.

</details>

---

## Going further

- Write the Square/Rectangle pair in real C++ with `setWidth`/`setHeight`,
  then write a function `void stretch(Rectangle& r)` that sets the width to
  10 and asserts the height did not change. Pass it a Square and watch the
  LSP violation happen in front of you.
- Design the Bird hierarchy correctly: a base `Bird` without `fly()`, a
  `FlyingBird` that adds it, and `Penguin`/`Sparrow` in the right places.
  How does code that only cares about flight change?
- Look up how C++'s standard library implements `std::stack`. It is a
  **container adapter** -- a wrapper that holds another container (by
  default `std::deque`) as a member and exposes only the stack operations.
  The standard library chose has-a for exactly the reason in this activity.
- Search for the phrase "composition over inheritance" and read one or two
  arguments for it. Then find one case where inheritance is still clearly
  the better tool -- what makes that case different?
