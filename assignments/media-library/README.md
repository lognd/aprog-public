# Media Library

A media collection is naturally a family of related things -- books, films,
albums -- that are all "a piece of media" but each carry their own details.
This assignment asks you to model that family with an abstract base class,
then build a separate `Library` class that catalogs a mix of them without
ever caring which concrete kind it is holding.

---

## Learning goals

- Design an abstract base class (`MediaItem`) with pure virtual functions and
  understand why an abstract class cannot be instantiated
- Write derived classes (`Book`, `Film`, `Album`) that publicly inherit from a
  base class and override its virtual functions
- Call overridden functions through a base class pointer or reference and see
  dynamic dispatch pick the correct derived implementation at run time
- Distinguish is-a (inheritance: `Book` is-a `MediaItem`) from has-a
  (composition: `Library` has-a collection of items)
- Recognize the "hiding" pitfall, where a derived function that does not
  exactly match the base signature fails to override it at all
- Explain why a non-owning pointer is the right tool when a class refers to
  objects it does not own

## Background

`MediaItem` is provided for you, complete, in `media-library.hpp`:

```cpp
class MediaItem {
public:
    MediaItem(std::string title, int year) : title_(std::move(title)), year_(year) {}
    virtual ~MediaItem() = default;

    virtual std::string kind() const = 0;
    virtual std::string summary() const = 0;

    std::string title() const { return title_; }
    int year() const { return year_; }

protected:
    std::string title_;
    int year_;
};
```

Two of its member functions end in `= 0`. That is a **pure virtual
function**: it has no body in `MediaItem` at all, and every non-abstract
class derived from `MediaItem` must supply one. A class with at least one
pure virtual function is an **abstract base class (ABC)** -- the compiler
will refuse to let you write `MediaItem m("x", 2000);` anywhere, because
there is no complete `kind()`/`summary()` to call. You can only ever hold a
`MediaItem` through a reference or pointer to a fully-formed derived object.

The base class constructor always runs before the derived class body starts
running. When you write `Book(std::string title, int year, ...)  :
MediaItem(std::move(title), year), ...`, the member initializer list is what
hands `title` and `year` up to `MediaItem`'s constructor -- `title_` and
`year_` are members of `MediaItem`, so only `MediaItem`'s own constructor is
allowed to initialize them directly.

## Task

### Part 1 -- Book, Film, Album

Declare and implement three classes, each publicly inheriting from
`MediaItem`:

| Class | Extra fields | Constructor signature |
|---|---|---|
| `Book` | `std::string author`, `int pages` | `Book(std::string title, int year, std::string author, int pages)` |
| `Film` | `std::string director`, `int minutes` | `Film(std::string title, int year, std::string director, int minutes)` |
| `Album` | `std::string artist`, `int trackCount` | `Album(std::string title, int year, std::string artist, int trackCount)` |

Each must override `kind()` and `summary()`, both marked `const override`.
`kind()` returns exactly `"Book"`, `"Film"`, or `"Album"`. `summary()` must
return **exactly** these formats (no trailing newline, one space where shown):

```
Book:  Book: "Dune" (1965) by Frank Herbert, 412 pages
Film:  Film: "Inception" (2010), directed by Christopher Nolan, 148 min
Album: Album: "Thriller" (1982) by Michael Jackson, 9 tracks
```

The general patterns:

```
Book:  Book: "<title>" (<year>) by <author>, <pages> pages
Film:  Film: "<title>" (<year>), directed by <director>, <minutes> min
Album: Album: "<title>" (<year>) by <artist>, <trackCount> tracks
```

Use `title()` and `year()` (inherited from `MediaItem`) plus your own
private fields to build these strings. `std::to_string` converts an `int` to
a `std::string`.

### Part 2 -- Library

Declare and implement a `Library` class that **has-a** collection of media
items -- this is composition, not inheritance. `Library` does not own the
items it catalogs: it stores `const MediaItem*`, non-owning pointers to
objects the caller constructed and continues to own. Nothing in this
assignment calls `new` or `delete`; `Library` only ever points at objects
that already exist somewhere else (a local variable, typically), and it is
the caller's job to keep those objects alive for as long as the `Library`
refers to them.

```cpp
Library lib;
Book b("Dune", 1965, "Frank Herbert", 412);
lib.add(b);          // lib now refers to b -- it does not copy or own it
```

`Library` needs:

- `void add(const MediaItem& item)` -- store a pointer to `item`
- `int count() const` -- how many items have been added
- `std::vector<std::string> summaries() const` -- one string per item, in
  the order added, each produced by calling `summary()` **through the base
  pointer**. This only works because `summary()` is virtual: even though the
  pointer's static type is `const MediaItem*`, calling `summary()` on it
  dispatches to `Book::summary()`, `Film::summary()`, or `Album::summary()`
  depending on what the pointer actually points at.

### The hiding pitfall

`override` is not just documentation -- it is a compiler check. If you write
a derived function whose signature does not exactly match the base
function's (wrong `const`-ness, wrong parameter types, a typo in the name),
the compiler will **not** treat it as an override. Instead you get a brand
new, unrelated function that happens to share a name and *hides* the base
one from lookup on the derived type. Two consequences follow, and both are
worth deliberately breaking your own code to see:

- Because the base class's pure virtual function is still unimplemented,
  your "derived" class is still abstract, and you will get a compiler error
  the moment you try to construct one -- not a silent bug, a hard stop.
- If you ever do get a hiding function to compile (for example, by also
  giving the base class a non-pure version), calling it through a
  `MediaItem*` would silently call the base version instead of yours,
  because hiding is resolved by the pointer's static type, not the object's
  real type.

Always write `override` on every function meant to override a base virtual
function. It turns the first failure mode above from a confusing abstract-class
error into a clear "does not override" compiler diagnostic.

### Why not a deeper hierarchy?

You might be tempted to add `PrintMedia : public MediaItem` or split `Book`
into `Paperback`/`Hardcover`. Resist it here. Deep inheritance hierarchies
are hard to reason about: every level adds another constructor to chain
through, another virtual function to keep in sync, and another place a
signature mismatch can silently hide a base function. `Library` solves the
"holds any kind of media" problem with **composition** instead -- a flat
vector of pointers -- and needs no inheritance at all. Prefer the shallowest
hierarchy that lets you use virtual dispatch, and reach for composition
(has-a) everywhere else.

## Files

| File | Purpose |
|------|---------|
| `media-library.hpp` | `MediaItem` is complete -- do not modify it. Declare `Book`, `Film`, `Album`, and `Library` here. |
| `media-library.cpp` | Implement `Book`, `Film`, `Album`, and `Library` here. |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./media-library_tests
```

The `SUBMISSION_DIR` variable tells CMake where to find your
`media-library.hpp` and `media-library.cpp`.

## Constraints

- Do not modify the `MediaItem` class in `media-library.hpp`.
- Do not use `new`, `delete`, templates, or exceptions (`throw`) anywhere.
- `Library` must store `const MediaItem*`, not copies of `Book`/`Film`/`Album`
  objects and not `std::string` summaries computed early -- `summaries()`
  must call `summary()` through the stored pointer each time it runs.
- `kind()` and `summary()` must be marked `override` in every derived class.
- Do not use `std::string` formatting shortcuts that change the required
  output text -- match the formats in the Task section exactly.

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `new`/`delete`/`template`/`throw` (source check) | 10 |
| Abstractness and dispatch through base pointer (compile-check) | 15 |
| Visible tests (Catch2) | 25 |
| Hidden tests (Catch2) | 50 |
| **Total** | **100** |

## Submission

Submit two files: `media-library.hpp` and `media-library.cpp`. Do not rename
either file.

## Going further

- Add a fourth kind, `Podcast` (host, episodeCount), without changing
  `Library` at all. That is the point of programming against the
  `MediaItem*` shape shared by every derived class (an "interface" in the
  general sense: a fixed set of calls something guarantees to support)
  instead of a `std::vector<Book>`, `std::vector<Film>`, ...
- Try commenting out `override` on `Book::summary()` and comparing the
  compiler error to what happens when you also remove `const`. Which one
  refuses to compile, and which one silently compiles into a different bug?
- `Library::summaries()` returns `std::vector<std::string>`. Rewrite it (on
  a scratch copy) to return `std::vector<const MediaItem*>` directly instead
  and have the caller format strings. What does that change about who is
  responsible for the format spec in the Task section?
