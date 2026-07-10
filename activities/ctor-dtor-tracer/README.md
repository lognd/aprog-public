# Activity: Ctor/Dtor Tracer

Every object you create in C++ has a lifetime: it comes into existence at
some point, and it eventually goes away. A **constructor** is a special
function that runs automatically the moment an object is created, used to set
up its initial state (for example, opening a file or initializing a member
variable). A **destructor** is a special function that runs automatically the
moment an object's lifetime ends, used to clean up (for example, closing that
file). This activity makes those two moments visible by having a handful of
tiny classes print a message every time their constructor or destructor runs,
so you can watch object lifetimes happen in the order the language actually
guarantees, not the order you might assume.

---

## Concepts covered

- Constructors and destructors as automatic, unavoidable lifecycle hooks
- Scope: how a variable's enclosing braces determine when it is destroyed
- Construction order (declaration order) vs. destruction order (reverse)
- Member objects: constructed before, destroyed after, the containing class's own body
- Temporaries: unnamed objects destroyed at the end of the full expression that created them
- Early `return` still runs destructors for locals already constructed (the basis of RAII)

## How it works

Each snippet is a complete, compilable C++ program. Every class in it prints
a line like `"A up"` from its constructor and `"A down"` from its destructor.
The launcher compiles and runs each snippet with `g++`, and you must type the
**exact** output, line by line, before it moves on. There is no partial
credit for "close enough" -- if your predicted output has a line out of
order, or missing, or extra, it will be marked wrong and you will see a hint
explaining exactly where your reasoning went astray.

This activity is intentionally the same shape as `enum-field-day` and
`cstring-vs-stdstring`: predict-the-exact-output, not multiple choice. The
"answer" is not a matter of opinion -- it is whatever the compiler actually
produces, which is exactly why this style of activity works so well for
building intuition about language rules.

## Getting started

```bash
python3 launch.py
```

You will be shown one C++ snippet at a time. Read the code carefully, trace
through it by hand (consider writing out each object's constructor and
destructor call on paper before typing anything), and type the program's
expected output. Press Enter after each line; when you believe you have
typed the full output, the launcher checks it.

## You will know you are done when...

After you correctly predict every snippet's output, the launcher prints a
passphrase. If your answer is wrong, you will see an explanation of the rule
you missed and a chance to try again.

## Hints

<details>
<summary>Hint 1 -- what is a "scope" exactly?</summary>

A **scope** is a region of code, delimited by a matching pair of curly braces
`{ }`, in which a name (like a variable) is valid. When execution reaches the
closing brace of the scope a local variable was declared in, that variable's
destructor runs (if it has one) -- even if that closing brace belongs to an
`if` block, a loop body, or just a bare `{ }` pair with no keyword attached to
it. This is the single rule that explains almost every snippet in this
activity.

</details>

<details>
<summary>Hint 2 -- why does destruction order reverse construction order?</summary>

If you declare `A a1; A a2;` in that order, `a2` is destroyed first, then
`a1`. This matters because `a2` might depend on `a1` still being alive (for
example, holding a pointer or reference to it, or being defined "in terms of"
it conceptually) -- destroying things in the reverse order they were built
guarantees that anything a later object might depend on is still valid while
that object is being cleaned up.

</details>

<details>
<summary>Hint 3 -- what is a "temporary" object?</summary>

A **temporary** is an unnamed object created to hold an intermediate value,
most often the direct result of a constructor call written inline (like
`A()` used directly as a function argument, with no variable name attached
to it). A temporary's lifetime normally ends at the end of the **full
expression** it appears in -- roughly, the entire statement, up to the
semicolon -- not at the end of whatever function it was passed into.

</details>

## Going further

- Add a second class `B` alongside `A`, give `Car` two members (an `Engine`
  and a `Battery`, say), and predict how the member construction/destruction
  order changes based on declaration order.
- Try wrapping a `return` inside a loop and predict how many constructor and
  destructor pairs run before the loop exits early.
- Look up the term RAII (Resource Acquisition Is Initialization) -- it names
  the technique of tying a resource's cleanup to an object's destructor so it
  happens automatically and reliably, no matter how the enclosing scope is
  exited. This activity's guarantee (locals are always destroyed when their
  scope ends) is exactly what makes RAII work, and it pairs directly with the
  `raii-file-guard` assignment.
