# Pattern Toolkit

A design pattern is a named, reusable solution to a recurring design problem.
This assignment asks you to implement three of the most common ones -- Strategy,
Observer, and Template Method -- each as a small, self-contained piece of C++.
All three are applications of the runtime polymorphism you learned in the
Polymorphism topic: an abstract base class with pure-virtual methods, concrete
subclasses that override them, and code that talks to the subclasses through a
non-owning base pointer or reference and lets the vtable pick the right
override at runtime.

None of the three parts uses dynamic memory. Every object lives on the stack or
inside a `std::vector`, and every polymorphic relationship is expressed with a
plain non-owning `Base*` or `const Base&`, exactly as in the previous topic. You
will not write `new`, `delete`, or `throw` anywhere.

---

## Learning goals

- Recognize Strategy, Observer, and Template Method as concrete uses of
  abstract base classes and virtual dispatch
- Pass behavior as an object (Strategy) so one algorithm can be reconfigured
  without being rewritten
- Register and notify a changing set of listeners through non-owning base
  pointers (Observer), including correct removal
- Let a base class own an algorithm's skeleton and defer specific steps to
  virtual hooks in subclasses (Template Method), the "Hollywood principle"
- Reinforce that virtual dispatch selects overrides at runtime through the
  vtable, and that non-owning pointers never imply ownership

## Background

All three patterns rest on the same machinery. An abstract base class declares
one or more pure-virtual methods. Concrete subclasses override them. Client code
holds a `Base*` or `Base&` and calls the virtual method; the compiler emits a
vtable lookup, so the override that runs depends on the object's real type at
runtime. The patterns differ only in how they arrange that machinery.

### Strategy

Strategy turns an algorithm's variable step into a separate object. Instead of
baking a comparison rule into a sort function, you pass in a comparison object
and the sort delegates to it. Swapping the object swaps the behavior, with no
change to the sort itself.

```
        +------------------+          +-------------------+
        |   sort_with()    | -------> |   SortStrategy    |  (abstract)
        | (the algorithm)  |  calls   |  before(a, b)     |
        +------------------+  before  +-------------------+
                                              ^
                          +-------------------+-------------------+
                          |                   |                   |
                    Ascending           Descending         ByAbsoluteValue
```

Use Strategy when you have one algorithm with a step that should vary
independently -- sorting orders, pricing rules, routing policies.

### Observer

Observer lets a subject broadcast changes to a set of listeners that register
themselves at runtime. The subject holds non-owning pointers to its observers
and calls a virtual hook on each one whenever its state changes. Observers can
attach and detach at any time.

```
        +---------------+  set_temperature(t)
        |  Thermometer  |----------------------+
        |  (subject)    |   notifies each      |
        +---------------+   attached observer  v
                                    +----------------------+
                                    |   Observer (abstract)|
                                    |  on_temperature(t)   |
                                    +----------------------+
                                        ^             ^
                                   HighAlarm     TemperatureLog
```

Use Observer when one object's changes must reach an open-ended, runtime-varying
set of dependents -- event systems, model/view updates, alarms.

### Template Method

Template Method fixes the outline of an algorithm in a base class and lets
subclasses fill in specific steps. The base class defines a non-virtual method
that calls virtual hooks in a fixed order. Subclasses override the hooks but
never the outline. This is the "Hollywood principle": don't call us, we'll call
you -- the base class calls the subclass's hooks, not the other way around.

```
        ReportGenerator::generate()   (fixed skeleton, not overridden)
              |
              +--> header()   (virtual hook -- subclass fills in)
              +--> body()     (virtual hook -- subclass fills in)
              +--> footer()   (shared, defined once in the base)
```

Use Template Method when several variants share an overall procedure but differ
in a few steps -- report formats, parsers, game turn loops.

---

## Task

Each part lives in its own header. Implement every member function and free
function declared in that header, inside the same header file.

### Part 1 -- Strategy (`sort_strategy.hpp`)

`SortStrategy` is an abstract base class with one pure-virtual method:

```cpp
virtual bool before(int a, int b) const = 0;
```

`before(a, b)` returns `true` when `a` should be ordered before `b`. Implement
three concrete strategies:

- `Ascending` -- `before(a, b)` is `a < b`.
- `Descending` -- `before(a, b)` is `a > b`.
- `ByAbsoluteValue` -- orders by absolute value, smaller magnitude first. When
  two values have equal absolute value (for example `-3` and `3`), break the tie
  by actual ascending value, so `-3` comes before `3`.

Also implement the free function:

```cpp
void sort_with(std::vector<int>& v, const SortStrategy& strategy);
```

`sort_with` sorts `v` in place so that every adjacent pair satisfies the
strategy's `before`. It must delegate every comparison to
`strategy.before(a, b)` -- it may not hardcode any ordering of its own. Any
correct comparison-based sort is fine. `sort_with` is **not** required to be
stable, so the relative order of elements the strategy considers equivalent is
unspecified.

### Part 2 -- Observer (`thermometer.hpp`)

`Observer` is an abstract base class:

```cpp
virtual void on_temperature(double temp) = 0;
```

`Thermometer` is the subject. Implement:

- `void attach(Observer* o)` -- registers `o` for future notifications. `o` is a
  non-owning pointer; the thermometer never allocates or frees it.
- `void detach(Observer* o)` -- removes `o` so it receives no further
  notifications. Does nothing if `o` was never attached.
- `void set_temperature(double temp)` -- calls `on_temperature(temp)` on every
  attached observer, in the order they were attached.

Implement two concrete observers:

- `HighAlarm(double threshold)` -- `count()` returns how many notified
  temperatures were **strictly greater than** `threshold`. A value equal to the
  threshold does not count.
- `TemperatureLog` -- records every notified temperature in order; `values()`
  returns them as a `const std::vector<double>&`.

Notification order must equal attach order, and `detach` must truly remove the
observer so it stops being notified.

### Part 3 -- Template Method (`report_generator.hpp`)

`ReportGenerator` is an abstract base class that owns the algorithm skeleton:

```cpp
std::string generate() const;   // non-virtual: do not override
```

`generate()` returns `header() + body() + footer()`, calling those three in that
exact order. `header()` and `body()` are protected pure-virtual hooks; `footer()`
is a protected non-virtual method defined once in the base class and shared by
every report. The exact strings are:

- `SalesReport::header()` returns `"=== Sales Report ===\n"`
- `SalesReport::body()` returns `"Total Sales: $1000\n"`
- `InventoryReport::header()` returns `"=== Inventory Report ===\n"`
- `InventoryReport::body()` returns `"Items In Stock: 42\n"`
- `footer()` (base class, shared) returns `"--- End of Report ---\n"`

So `SalesReport().generate()` returns exactly:

```
=== Sales Report ===
Total Sales: $1000
--- End of Report ---
```

The hidden tests compare `generate()` output byte for byte, so reproduce the
strings, including the trailing newlines, precisely.

## Files

| File | Purpose |
|------|---------|
| `sort_strategy.hpp` | Part 1 -- Strategy; edit and implement here |
| `thermometer.hpp` | Part 2 -- Observer; edit and implement here |
| `report_generator.hpp` | Part 3 -- Template Method; edit and implement here |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
mkdir build && cd build
cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./pattern-toolkit_tests
```

The `SUBMISSION_DIR` variable tells CMake where to find your three headers.

## Constraints

- Do not modify the class or function signatures in the three headers.
- Do not use `new`, `delete`, or `throw` anywhere in any of the files.
- Hold observers only as non-owning pointers; never take ownership.
- Do not override `ReportGenerator::generate()`; override only the hooks.

---

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `new`/`delete`/`throw` (source check) | 10 |
| Visible tests (Catch2) | 30 |
| Hidden tests (Catch2) | 60 |
| **Total** | **100** |

## Submission

Submit three files, all with their original names:

- `sort_strategy.hpp`
- `thermometer.hpp`
- `report_generator.hpp`

---

## Going further

- Add a `ByLastDigit` strategy that orders ints by their least-significant
  decimal digit and pass it to `sort_with`. Notice you changed no sort code.
- Add a `RangeAlarm(double low, double high)` observer that counts
  temperatures falling inside a band, attach it alongside `HighAlarm`, and
  confirm both fire on the same `set_temperature` call.
- Add a `SummaryReport` whose `body()` combines several lines. What did you have
  to write, and what did you get for free from the base class?
- Detach an observer from inside another observer's `on_temperature` and reason
  about what happens to the in-progress notification loop.
