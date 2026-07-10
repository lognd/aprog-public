# Activity: Pillar Identification

Object-oriented programming (OOP) is a style of building software out of
**objects**: bundles of data plus the functions that operate on that data.
In C++, you describe a kind of object by writing a **class** -- a blueprint
that says what data each object of that kind stores (its **fields**) and
what it can do (its **methods**, which are just functions attached to the
class). Before writing any C++ class syntax, though, you need the
vocabulary that the entire OOP world is discussed in: five recurring design
ideas usually called the five pillars.

This activity presents concrete software scenarios -- no code -- and asks
you to name the pillar each one demonstrates: abstraction, encapsulation,
inheritance, polymorphism, or composition. Naming them reliably, especially
telling abstraction and encapsulation apart, is the goal.

---

## Background

### Abstraction -- hide complexity behind a simple interface

An **interface** is the set of things the outside world can ask an object
to do -- its public methods. **Abstraction** means designing that interface
to be simple, so users of the object never have to think about the
complicated machinery inside.

A radio has knobs: tune to a frequency, turn it on or off. Nobody using a
radio thinks about demodulation circuits. A `Radio` class built the same
way exposes `tune(frequency)` and `power(on_off)` and keeps all the
signal-processing complexity out of sight. The user's mental model stays
tiny; the complexity still exists, but only the class author deals with it.
Abstraction is about managing complexity: choosing what the user must know
and hiding everything else.

### Encapsulation -- protect data behind controlled access

**Encapsulation** means bundling data together with the only methods
allowed to touch it, and blocking direct outside access to that data. In
C++, the `private` keyword does the blocking: a private field cannot be
read or written from outside the class.

A `BankAccount` class stores `balance` as a private field. Outside code
cannot do `account.balance = -1000000`. It can only call
`deposit(amount)` and `withdraw(amount)`, and those methods can validate:
reject a negative deposit, refuse an overdraft. The data can never be put
into a nonsense state, because every change goes through a checkpoint.

### The classic trap: abstraction vs encapsulation

These two get confused constantly, because they usually appear together in
the same class. The distinction:

- Abstraction is about **complexity**: present a simple view, hide the
  complicated machinery. It answers "what does the user need to think
  about?"
- Encapsulation is about **access**: make data private, force every change
  through validating methods. It answers "who is allowed to touch this
  data, and how?"

A `Stack` class whose interface shows only `push`/`pop`/`top` while
secretly being implemented with a `std::vector` is demonstrating
abstraction -- the implementation choice is hidden, and could be swapped
without any user noticing. A `Logger` whose internal buffer no outside code
can read or modify is demonstrating encapsulation -- the emphasis is on
forbidden access. When a scenario stresses "the user does not need to know
how it works inside," think abstraction. When it stresses "no other code
can read or modify this field directly," think encapsulation. Several
questions in this activity sit right on that boundary on purpose.

### Inheritance -- build a new class by extending an existing one

**Inheritance** lets you declare that a new class is an extension of an
existing one, automatically reusing all its fields and methods. The
existing class is called the **base class** (or parent); the new one is the
**derived class** (or child).

If `Vehicle` has `make`, `model`, `year`, and a `describe()` method, then
declaring `Car` as a class that inherits from `Vehicle` gives `Car` all of
those for free; `Car` just adds what is specific to cars. Inheritance
models an **is-a** relationship: a Car is-a Vehicle. It should only be used
when that is genuinely true -- a later activity (is-a-has-a) digs into how
that can go wrong.

### Polymorphism -- one call, many behaviors

**Polymorphism** (from Greek, "many forms") means the same method call can
behave differently depending on what kind of object it lands on -- without
the caller ever checking which kind it has.

Picture a list holding a mix of `Circle`, `Square`, and `Triangle` objects,
all handled through their common base class `Shape`. A loop calls
`shape->draw()` on each element, and each object draws itself correctly --
circle code for circles, square code for squares. The loop contains no
if/else chain asking "which type is this?"; the right version of `draw()`
is chosen automatically at run time. Inheritance is usually the mechanism
that makes this possible (all three classes derive from `Shape`), but the
pillar itself is the "one interface, many behaviors" effect.

### Composition -- build objects out of other objects

**Composition** means a class contains another object as one of its fields
and delegates work to it. It models a **has-a** relationship.

A `Car` does not inherit from `Engine` -- a car is not a kind of engine.
Instead `Car` has an `Engine` field, and `Car::start()` internally calls
`engine_.start()`. Complex objects get assembled from simpler parts, each
independently understandable and testable. Experienced designers often
say "favor composition over inheritance": when all you want is to reuse
another class's functionality, holding one as a part is usually safer than
claiming to be one.

---

## Concepts covered

- Abstraction: hiding complexity behind a simple, stable interface
- Encapsulation: private data plus validating methods as the only access
  path
- The abstraction-vs-encapsulation boundary -- the classic exam trap
- Inheritance as an is-a relationship that reuses a base class's members
- Polymorphism: one method call dispatching to different behavior per
  object type
- Composition as a has-a relationship: objects assembled from owned parts

---

## How it works

The launcher shows you eleven scenario questions. Each describes a concrete
piece of software design in plain English -- a class, what it exposes, what
it hides, what it contains, or what it extends. No code appears anywhere.

Every prompt ends with the same explicit option list:

```
Type exactly one of: abstraction / encapsulation / inheritance / polymorphism / composition
```

Type the pillar name exactly. A wrong answer gets feedback explaining the
specific distinction you missed -- especially on the
abstraction-vs-encapsulation questions, where the feedback spells out which
signal word in the scenario points the other way. A correct answer unlocks
a fuller explanation. Answer all eleven correctly and the launcher decrypts
and prints the passphrase.

---

## Getting started

```bash
python3 launch.py
```

Read each scenario twice before answering. The pillar is always signaled by
specific phrases -- "hides its internals" reads differently from "cannot be
modified directly from outside," and "extends" reads differently from "has
a field of type."

---

## You will know you are done when...

The launcher prints `All correct.` followed by the passphrase between two
horizontal rules. Record the passphrase -- it is your proof of completion.

---

## Hints

<details>
<summary>Hint 1 -- signal words for each pillar</summary>

Abstraction: "simple interface," "does not need to know how it works,"
"implementation detail is invisible." Encapsulation: "private field,"
"cannot read or modify directly," "only way to change it is through."
Inheritance: "extends," "derives from," "reuses the base class's methods."
Polymorphism: "the same call," "each object responds in its own way,"
"without checking which type." Composition: "has a," "contains,"
"owns a ... as a member," "delegates to."

</details>

<details>
<summary>Hint 2 -- the abstraction vs encapsulation tiebreaker</summary>

Ask: is the scenario's emphasis on what the user has to THINK about, or on
what outside code is ALLOWED TO TOUCH? Simplifying the mental model is
abstraction. Restricting access to data is encapsulation. If a scenario
mentions private fields but spends its words on how simple the interface
is or how swappable the implementation is, the tested answer is
abstraction.

</details>

<details>
<summary>Hint 3 -- inheritance vs polymorphism</summary>

Inheritance is the relationship (Car extends Vehicle). Polymorphism is
the run-time effect that relationship enables (calling `describe()` through
a `Vehicle` reference and getting `Car`'s version). If the scenario only
describes extending and reusing, answer inheritance. If it describes the
same call behaving differently per object, answer polymorphism -- even
though inheritance is involved behind the scenes.

</details>

---

## Going further

- Take any two pillars and find a real class in the C++ standard library
  that demonstrates both. (`std::vector` is a good start: what does it
  abstract away, and what does it encapsulate?)
- Write a one-paragraph scenario of your own for each pillar, in the style
  of this activity's questions, and test a classmate. Writing scenarios
  that are NOT ambiguous is harder than answering them.
- The Shape/draw() scenario is the classic motivating example for virtual
  functions in C++. Look up how the language implements this dispatch (the
  keyword is `virtual`, the mechanism is called a vtable -- a hidden table
  of function pointers each object carries a reference to) and be ready for
  it when the course reaches OOP syntax.
- Find a class you wrote earlier this semester (even a plain struct) and
  identify which pillars it already uses -- most code uses abstraction long
  before its author knows the word.
