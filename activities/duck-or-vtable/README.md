# Activity: Duck or Vtable

C++ gives you two very different ways to write one piece of code that
works with several different types. One way uses inheritance and a shared
base class -- the "interface" approach. The other uses templates and asks
nothing more than "does this type support the operations I need?" -- an
idea usually called duck typing. Both let you avoid writing the same logic
over and over for every type, but they make very different trade-offs, and
this activity is about learning to tell, precisely, which one a piece of
code is using and what that choice costs or buys you.

## Concepts covered

- Interfaces via an abstract base class (a class with at least one pure
  virtual function, meaning it cannot be instantiated directly and exists
  only to declare a required set of methods)
- Duck typing: writing code that only requires a type to support the
  operations actually used, with no shared base class required at all
- Template instantiation: the compiler generating a separate, concrete
  copy of a function template for each distinct type it is called with
- Compile-time decisions (template instantiation, overload resolution,
  default arguments) vs. run-time decisions (virtual dispatch through a
  vtable)
- Heterogeneous storage (one container holding several different concrete
  types) as something only the interface approach supports directly
- The small per-call runtime cost of a vtable lookup, and why templates
  avoid it

## How it works

You are shown eight short C++ programs, each using either a virtual
interface or a function template to handle more than one type uniformly.
Every question asks something pointed and specific about the code shown:
does it compile, is the decision made at compile time or run time, can a
single container hold mixed concrete types, or which version pays a
runtime cost per call. Each question gives you a short list of exact
answers to choose from -- type one of them exactly as written.

If you answer incorrectly, you are shown a targeted explanation of why
your answer does not fit this specific snippet, and you can try again. A
correct answer unlocks a fuller explanation connecting the snippet to the
underlying mechanism -- the vtable (a hidden per-class table of function
pointers used to find the correct override at runtime) for the interface
questions, or template instantiation for the duck-typing questions.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have answered all eight questions correctly and the activity prints
your passphrase.

## Hints

- For "does this compile?" questions about a template, mentally substitute
  the real type in for the template parameter and read the function body
  as if you had written it by hand for that exact type. If that
  substituted code would not compile, neither does the template
  instantiation.
- For "does this compile?" questions about an interface, check whether the
  type in question actually derives from the base class -- having a method
  with a matching name and signature is not enough on its own; the
  inheritance relationship has to actually exist.
- "When is the decision made?" almost always comes down to: does the
  compiler need to know the concrete type in advance to generate this
  code (compile time), or can the same compiled code correctly handle
  different concrete types depending on what it is given while running
  (run time)?
