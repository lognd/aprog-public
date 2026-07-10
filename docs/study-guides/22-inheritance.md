# Study Guide 22: Inheritance (ABC, drawbacks, composition)

This module covers the C++ mechanics of inheritance and its two famous
failure modes: name hiding (a same-named function that silently is not an
override) and object slicing (copying a derived object into a base-typed
slot cuts off everything derived). The media-library assignment applies
abstract base classes, dynamic dispatch, and non-owning composition
together.

## Know before you start

- Is-a vs. has-a and the Liskov Substitution Principle [assumed: row 20 --
  OOP Vocab & Theory]
- Constructors/destructors, member construction order, and `const` member
  functions [assumed: row 21 -- OOP Implementation in C++]
- References vs. pointers and pass-by-value vs. by-reference [assumed:
  row 11 -- Pointers]
- `std::vector` element storage and copying on insertion [assumed: row 7 --
  Standard Library Types]

## Taught here

Concept: static vs. dynamic type and virtual dispatch
- Know that a variable's static type is the type written in the code (all
  the compiler knows at compile time), while its dynamic type is the
  actual concrete type of the object it refers to at runtime -- given
  `Derived d; Base& ref = d;`, the static type of `ref` is `Base&` and the
  dynamic type is `Derived`.
- Know that non-virtual calls are resolved using the static type alone,
  while `virtual` calls through a base reference or pointer are resolved
  using the dynamic type, running the derived override.
- Know that most compilers implement virtual dispatch with a vtable -- a
  per-class table of function pointers consulted at runtime to find the
  correct override.

Concept: overriding vs. hiding
- Know that a derived function only overrides a base virtual function when
  its signature matches exactly: same name, same parameter types, and the
  same `const` qualification (the `const` on a member function is part of
  its signature).
- Know that any mismatch -- most commonly a missing `const` -- silently
  creates a hide instead: a separate, unrelated function that shares the
  name, hides the base name on direct derived calls, but never participates
  in virtual dispatch.
- Know that marking intended overrides with the `override` keyword makes
  the compiler reject signature mismatches instead of silently compiling a
  hide -- always use it.
- Know that a virtual call made from inside a base class constructor always
  resolves to the base version, because the derived part of the object has
  not been constructed yet and its override could touch uninitialized
  derived fields.
- Know that `protected` members are accessible to derived classes but
  hidden from all other outside code.

Concept: object slicing
- Know that slicing happens when a derived object is copied into something
  declared as its base type: only the base-class part survives, and every
  derived-added field and overridden behavior is silently cut off,
  producing a genuine, complete base object.
- Be able to spot the three places a slicing copy happens: `Base b =
  someDerived;`, a by-value `Base` function parameter receiving a derived
  argument, and insertion into a `std::vector<Base>` (whose slots are
  exactly `sizeof(Base)` bytes).
- Know that pass-by-reference (`Base&`) and pointers (`Base*`) make no copy
  and therefore never slice -- they still refer to the original, complete
  derived object.
- Know that a `std::vector<Base*>` of non-owning pointers stores only
  addresses and never slices, unlike `std::vector<Base>` which slices every
  insertion.
- Know that a slicing copy runs the base class's own copy constructor,
  which only knows the base's fields -- derived fields are not copied
  because the base copy constructor has no knowledge they exist.

Concept: abstract base classes and composition
- Know that a pure virtual function (`= 0`) has no body in the base class
  and must be supplied by every non-abstract derived class, and that a
  class with at least one pure virtual function is an abstract base class
  (ABC) that the compiler refuses to instantiate directly.
- Know that an ABC can only be used through a reference or pointer to a
  fully constructed derived object.
- Know that the base class constructor always runs before the derived
  class body, and that the member initializer list (`Derived(...) :
  Base(args), ...`) is how a derived constructor hands arguments up,
  because only the base's own constructor may initialize the base's
  members.
- Be able to write derived classes that override pure virtual functions
  with `const override` and produce exact required output formats.
- Know that a catalog class holding `const MediaItem*` non-owning pointers
  is composition (has-a), not inheritance, and that non-owning means the
  caller constructed the objects, continues to own them, and must keep
  them alive as long as the catalog refers to them -- no `new`/`delete`
  involved.

## Study checklist

- [ ] Given a base reference to a derived object, predict which version of
      a virtual and a non-virtual function each call runs.
- [ ] Explain how a missing `const` turns an intended override into a hide,
      and how `override` prevents it.
- [ ] Explain why virtual calls in a base constructor use the base version.
- [ ] List the three code shapes that cause slicing and the two shapes that
      never do.
- [ ] Explain why `MediaItem m("x", 2000);` fails to compile.
- [ ] Explain what "non-owning pointer" obligates the caller to do.

## Practiced in

`hiding-hunt`, `slice-of-life`, `media-library`
