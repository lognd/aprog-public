# Activity: Encapsulation Audit

**Encapsulation** is the idea of bundling an object's data together with the
code that is allowed to change it, and restricting direct access to that data
from the outside. It is one of the foundational ideas in object-oriented
programming (writing code as interacting objects, each responsible for its
own data). Each question below shows a small C++ class snippet -- some
well-designed, some with a specific, common flaw -- and asks you to diagnose
exactly what is wrong, or confirm that nothing is. This is the kind of
judgment a code reviewer exercises on every pull request that touches a
class's public interface.

---

## Concepts covered

- **Invariant**: a rule about an object's internal state that must always
  hold true (for example, "a bank balance can never go negative")
- Public data members vs. private data with controlled access
- **Const-correctness**: marking member functions `const` when they do not
  modify the object, so the compiler and other programmers can trust that
  promise
- **Getter**: a method whose job is to let outside code read a piece of an
  object's state
- The "leaky getter" trap: returning a non-const reference from a getter,
  which lets outside code mutate private data anyway
- Recognizing correctly-encapsulated classes, not just broken ones

## How it works

Each question shows a short C++ class (or struct, or a class plus a related
free function) and a description of what happens when it is used. You must
identify the issue by typing **exactly one** of the listed options:

- `public data with no invariant enforcement`
- `missing const`
- `leaky getter returning non-const reference`
- `nothing wrong`

Not every snippet has a bug. Recognizing a well-encapsulated class is just as
much a skill as spotting a broken one, and this activity mixes both so you
cannot simply guess "something is wrong" every time.

## Getting started

```bash
python3 launch.py
```

Read each snippet carefully. Ask yourself, in order: Is any field directly
public with no validation on it? Is any method that clearly does not modify
the object missing a `const` marker? Does any method hand back a reference
that lets outside code bypass the class's own rules? If none of those apply,
the answer is `nothing wrong`.

## You will know you are done when...

Once you answer every question correctly, the launcher prints a passphrase.
Wrong answers show an explanation of why that option does not fit this
particular snippet, and you get to try again.

## Hints

<details>
<summary>Hint 1 -- invariant vs. access control are two different things</summary>

Making a field `private` and only reachable through a setter method does not
automatically mean the class's invariants are protected. A setter that
accepts absolutely any value with no checks (for example, `setRadius(double
r) { radius_ = r; }` with no check that `r` is non-negative) still lets the
object end up in an invalid state -- it just makes you go through an extra
function call to get there. Look for setters that validate, clamp, or
reject bad input, not just setters that exist.

</details>

<details>
<summary>Hint 2 -- what exactly does returning a reference "leak"?</summary>

A **reference** is an alias for an existing variable -- not a copy of its
value. If a public method returns a non-const reference to a private field
(for example, `std::vector<std::string>& members() { return members_; }`),
anyone who calls that method gets a live handle to the actual private data,
and can call mutating operations on it directly, completely bypassing
whatever validation the class's own methods might otherwise perform. Returning
a plain value (a copy), or a `const` reference, closes this hole.

</details>

<details>
<summary>Hint 3 -- why does `const` matter here at all?</summary>

Marking a method `const` is a promise, checked by the compiler, that calling
it will not modify the object. This matters practically: a method that is
NOT marked `const` cannot be called at all through a `const Type&` or `const
Type*` -- a situation that comes up constantly once other code starts
passing objects around by const reference to avoid unnecessary copying. A
getter that forgot `const` is not just a style nitpick; it can make a
perfectly correct, read-only method uncallable in an otherwise reasonable
context.

</details>

## Going further

- For each snippet marked `public data with no invariant enforcement` or
  `leaky getter returning non-const reference`, write the fixed version of
  the class yourself.
- For the `missing const` snippets, add the missing `const` and try calling
  the method through a `const Type&` parameter to confirm it now compiles.
- Think of an invariant for a class you have written yourself (a `Grade`
  that must stay between 0 and 100, a `Percentage` that must stay between 0
  and 1, and so on) and write both a broken version (no validation) and a
  fixed version (validated in the setter).
