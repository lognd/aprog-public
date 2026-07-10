# Activity: Value Category Taxonomy

`big5-tracer` showed you that a class can have up to five special member
functions, and that the compiler silently picks one of them -- the copy
constructor, the move constructor, and so on -- every time you construct,
copy, move, or assign an object. But *how* does the compiler decide
*which* one runs? The answer is not about the class at all. It is about
the argument you hand it: every expression in C++ carries a **value
category** (lvalue, xvalue, or prvalue), and that category is what
overload resolution reads to pick copy vs. move. This activity is the
theory underneath everything `big5-tracer` made you predict.

## Concepts covered

- Identity (can you take its address, refer to it again later?) and
  movable-from-ness (is nothing else going to look at it again?) as the
  two independent questions that generate the whole taxonomy
- The three leaf categories: lvalue, xvalue, prvalue
- The two composite categories: glvalue (has identity) and rvalue
  (movable-from)
- Classifying real expressions, including the string-literal surprise
- Which reference type (`T&`, `const T&`, `T&&`) binds which category
- How value category drives overload resolution between `f(const T&)`
  and `f(T&&)` -- the exact mechanism behind copy vs. move selection
- `std::move` as a cast that changes nothing by itself
- C++17 guaranteed copy elision as prvalue materialization

## Background

A **value category** is a property of an *expression*, not of an object.
The same variable `x` can appear in an expression that is an lvalue
(`x`), in one that is an xvalue (`std::move(x)`), or inside one that
produces a prvalue (`x + 1`) -- the object `x` never changes, but each
expression that mentions it has its own category.

Every category in C++ falls out of exactly two yes-or-no questions asked
about an expression:

1. **Identity** -- does the expression refer to an object you could take
   the address of (`&expr`) and refer to again later, whether by its
   name, through a reference, or through something like array
   subscripting?
2. **Movable-from** -- is it safe to steal whatever resources the
   referred-to object owns, because nothing else is going to look at it
   again after this point?

An expression that has identity is called a **glvalue** ("generalized
lvalue"). An expression that is movable-from is called an **rvalue**.
Those two composite groups overlap, and the overlap is exactly where the
interesting category lives:

```
        HAS IDENTITY (glvalue)          MOVABLE-FROM (rvalue)
        ,--------------------,        ,----------------------,
       /                      \      /                        \
      /      lvalue            \    /            prvalue        \
     |     (x, a[0], *p)         \  /       (42, x + 1, T())      |
     |                          ,--`--,                           |
     |                         / xvalue \                         |
      \                       | std::move(x) |                   /
       \                       \           /                    /
        \                       `--------`                     /
         `----------------------------------------------------`
```

`lvalue` sits in the identity circle only: `x` has identity (you can
write `&x`), but nothing marks it as disposable. `prvalue` sits in the
movable-from circle only: `42` has no identity (`&42` does not compile),
so it is automatically movable-from -- there is nothing else that could
possibly still be looking at it. `xvalue` sits in the overlap: it has
identity (`std::move(x)` still refers to `x`, and you could take its
address through the reference `std::move` produces) *and* it carries the
movable-from signal.

<details>
<summary>Why does the intersection even exist? A one-line history</summary>

C++98 only needed one split: lvalue (things with names and addresses) vs.
rvalue (temporaries). That was enough because C++98 had no concept of
"moving" -- copying was the only option, so there was no reason to
distinguish "safe to steal from" as its own axis. C++11 introduced move
semantics, which needed a way to say "this thing has a name and an
address, but I promise nothing will look at it again -- steal its guts."
That need is exactly what created xvalue, and forced the taxonomy to
split into the five categories (lvalue, xvalue, prvalue, glvalue, rvalue)
you see today.

</details>

## Classifying one expression, step by step

Take `std::move(s).member`, where `s` is a local variable of some struct
type with a data member called `member`.

1. Start from the inside: `s` by itself is a named variable. Ask
   identity -- yes, `&s` compiles. Ask movable-from -- no, nothing marks
   it as disposable. Identity + not movable-from = **lvalue**.
2. `std::move(s)` casts that lvalue to an rvalue reference. Identity is
   preserved (it still refers to `s`, and you can take its address
   through the reference), and now it *is* movable-from, because
   `std::move` is the language's way of saying "treat this as
   disposable." Identity + movable-from = **xvalue**.
3. `.member` accesses a piece of the object the expression before the dot
   refers to. Member access preserves the value category of the object it
   is applied to: since `std::move(s)` is an xvalue, `std::move(s).member`
   is *also* an xvalue -- it still names a real subobject (identity), and
   it still carries the movable-from signal from the cast.

That is the exact mechanism a move constructor uses to move an individual
member out of a moved-from object:
`MyClass(MyClass&& other) : member(std::move(other).member) {}`.

## `std::move` is a cast, nothing more

The single most common misconception in this whole topic is that
`std::move(x)` *performs* a move -- that it reaches into `x` and steals
something right there on the spot. It does not. `std::move` is, under the
hood, essentially `static_cast<T&&>(x)`: a compile-time reinterpretation
of the expression's category, with **zero runtime effect** of its own. If
you write `std::move(x);` as a standalone statement and never pass the
result to anything, `x` is completely untouched -- nothing was freed,
nothing was zeroed, nothing moved.

What `std::move` actually buys you is a ticket into a different overload.
Casting `x` from lvalue to xvalue makes it eligible for an `f(T&&)`
overload that a plain lvalue could never bind to. The *actual* stealing
-- swapping a pointer, nulling out the source, whatever the class's move
constructor decides to do -- happens entirely inside whichever function
overload resolution ends up calling as a result of the cast. `std::move`
just makes that function reachable; it never runs it.

## The payoff: guaranteed elision is not "the move got skipped"

Recall the `big5-tracer` snippet built around this pattern:

```cpp
Tracer make_tracer(int id) {
    return Tracer(id);   // Tracer(id) is a prvalue, written directly here
}

Tracer t = make_tracer(7);
```

That snippet printed exactly one `ctor 7` line -- no `move-ctor` line at
all, even compiled with no optimizations. It is tempting to describe that
as "the compiler was nice enough to skip the move," the same way you
might describe Named Return Value Optimization for a return of an
already-named local. But that is not what happened here, and the
distinction matters.

Since C++17, a prvalue is not defined as a temporary object that then
gets copied or moved somewhere else. It is defined as a *recipe* for
initializing an object -- and that recipe is not carried out until it
**materializes** directly into its final storage location. `return
Tracer(id);` never constructs an intermediate `Tracer` that then has to
be moved into `t`'s memory. The recipe `Tracer(id)` propagates all the
way out to `t`'s storage in the caller, and the `Tracer` constructor runs
exactly once, directly there. There was structurally only ever one
object -- nothing to move, because there was never a second one to move
*from*. This is **mandatory** under the C++17 standard for a prvalue
written directly in a `return` statement, not merely a permitted
optimization (that older, optional kind of elision still exists too, for
returning an already-named local variable, but it is a different rule).

## How it works

You are given thirteen questions covering the two-question model, the
composite categories, classification drills on real code fragments,
reference-binding rules, overload resolution, `std::move`, and guaranteed
elision. Each question shows a short code fragment (or a small set of
matched fragments) and asks you to pick the exact right answer from an
explicit list of choices. Type the choice exactly as printed, including
any parenthetical.

## Getting started

```bash
python3 launch.py
```

Answer each question exactly as printed in its list of choices. A wrong
answer explains what specific misconception it reflects, then lets you
try again.

## You will know you are done when...

You have correctly answered all thirteen questions and the activity
prints your passphrase.

## Hints

<details>
<summary>Hint 1 -- the only two questions that matter</summary>

For every expression, ask (1) does it have identity -- can you take its
address and refer to it again later? and (2) is it movable-from -- is
nothing else going to look at it again? Every category in this activity
falls out of those two answers alone. Ignore whether something is named,
whether it is `const`, and where it lives in memory -- none of those
axes distinguish lvalue from xvalue from prvalue.

</details>

<details>
<summary>Hint 2 -- the literals table</summary>

| Expression       | Identity? | Movable-from? | Category |
|------------------|-----------|----------------|----------|
| `42`             | no        | yes            | prvalue  |
| `"hello"`        | yes (static storage duration) | no | lvalue |
| `x` (named var.) | yes       | no             | lvalue   |
| `x + 1`          | no        | yes            | prvalue  |
| `std::move(x)`   | yes       | yes            | xvalue   |

</details>

## Going further

- Print `decltype(expr)` for a handful of the expressions in this
  activity (`decltype(x)`, `decltype((x))` -- note the extra
  parentheses -- `decltype(std::move(x))`) and read up on the one-line
  rule: `decltype` on a parenthesized lvalue expression gives you back a
  reference type, which is `decltype`'s way of revealing the underlying
  value category in the type system itself.
- `std::forward` is the next mystery this activity deliberately leaves
  open: it exists to solve a problem that only shows up inside template
  functions taking `T&&` parameters (so-called "forwarding references,"
  which look identical to ordinary rvalue references but follow
  different binding rules). `std::forward` is not taught here -- it needs
  template type deduction first -- but now that you can name every value
  category on sight, you have everything you need to understand *why* a
  template function cannot just use `std::move` on its parameter and call
  it done.
- Cross-reference: `big5-tracer` (the whole activity this one explains
  the theory behind), `rule-of-five-whodunit` (every "missing move
  constructor" bug there is really a value-category story), and
  `ctor-dtor-tracer` (watch identity and lifetime interact directly).
  Also look at `unique-ptr-from-scratch`: its tests can assert "the
  source is empty after a move" specifically because a move constructor
  is only ever selected when the argument is an xvalue or prvalue --
  something the caller has already promised not to look at again.
