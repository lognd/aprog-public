# Pattern Toolkit

A design pattern is not a rule imposed from outside -- it is the shape code
takes when someone finally refactors (restructures existing code without
changing what it does) away from a mess that grew out of perfectly
reasonable choices. This assignment shows you three such messes first, lets
you feel why the next feature request makes them worse, and only then asks
you to implement the pattern that fixes it. All three are applications of
the runtime polymorphism you learned in the Polymorphism topic: an abstract
base class with pure-virtual methods, concrete subclasses that override
them, and code that talks to the subclasses through a non-owning base
pointer or reference and lets the vtable (the hidden table of function
pointers the compiler attaches to a class with virtual functions, used to
find the correct override) pick the right override at runtime.

None of the three parts uses dynamic memory. Every object lives on the stack
or inside a `std::vector`, and every polymorphic relationship is expressed
with a plain non-owning `Base*` or `const Base&`, exactly as in the previous
topic. You will not write `new`, `delete`, or `throw` anywhere.

---

## Learning goals

- Recognize code smells (a code smell is a pattern in working code that is
  not a bug but signals that a change will be painful to make safely) --
  specifically shotgun surgery, copy-paste divergence, and rigidity -- that
  motivate Strategy, Observer, and Template Method
- Pass behavior as an object (Strategy) so one algorithm can be reconfigured
  without being rewritten
- Register and notify a changing set of listeners through non-owning base
  pointers (Observer), including correct removal
- Let a base class own an algorithm's skeleton and defer specific steps to
  virtual hooks in subclasses (Template Method), the "Hollywood principle"
- Reinforce that virtual dispatch selects overrides at runtime through the
  vtable, and that non-owning pointers never imply ownership

## Background

All three patterns rest on the same machinery: an abstract base class
declares one or more pure-virtual methods, concrete subclasses override them,
and client code holds a `Base*` or `Base&` and calls the virtual method so
the override that runs depends on the object's real type at runtime. Rather
than presenting that machinery cold, each part below starts from working
code that grew organically -- one reasonable decision at a time -- until it
became painful to extend. Read the corresponding file in `assets/legacy/`
before you start each part; the pattern you implement is the refactor that
removes the pain.

### Strategy -- from `legacy/sort_modes.cpp`

`sort_numbers` began in 2022 as a single ascending sort. In 2023 the finance
team asked for a descending mode, so the fastest fix was to copy the loop
and flip one comparison. In 2024 the physics module needed sorting by
magnitude, so the ascending loop got copied again with `std::abs` sprinkled
in. The function still compiles and still works -- that is exactly the
problem. It is one `switch` over three near-identical copies of the same
insertion sort, with a `// TODO: add another mode??` comment marking where
the next copy would go.

Now suppose the next request arrives: add a fourth mode that sorts by least
significant digit. Doing it the way the file has always been extended means:

1. Add a new enumerator to `SortMode`.
2. Add a new `case` to the `switch`.
3. Copy the entire loop body a fourth time and change the comparison.
4. Update every call site that might want to expose the new mode.

Four places to touch for one new rule, and nothing stops a fifth mode from
being pasted in slightly wrong -- for example, comparing `std::abs(v[j - 1])
>= std::abs(key)` instead of `>` would silently break the stability
guarantee, and nothing in the function's shape would catch it.

**The smell:** shotgun surgery. One conceptual change (add an ordering rule)
requires editing one giant function in multiple places, and the loop body is
duplicated verbatim except for a single comparison.

**The fix:** Strategy turns an algorithm's variable step into a separate
object. Instead of baking a comparison rule into the sort function, you pass
in a comparison object and the sort delegates to it. Swapping the object
swaps the behavior, with no change to the sort itself -- and a new mode is a
new class, not a new copy of the loop.

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

### Observer -- from `legacy/thermometer_v1.cpp`

`ThermometerV1::set_temperature` began as one line: print the reading. Ops
then asked for a log of every reading, so a `std::vector<double>` got added
and appended to inline. Safety then asked for a high-temperature alarm, so a
counter and an `if` got added inline too. The function still works, and the
comment left in the file says it plainly: `// TODO: marketing wants SMS
alerts too, add param?? another bool??`

Now suppose that SMS request actually lands, plus a "quiet hours" flag that
suppresses the console print but keeps logging and alarms. Doing it the way
the file has always been extended means:

1. Add an SMS client member and a call to it inside `set_temperature`.
2. Add a `bool` parameter (or another member flag) for quiet hours.
3. Wrap the existing console `std::cout` line in a conditional on that flag.
4. Update every constructor call site to pass the new parameter or configure
   the new member.
5. Write a test for the alarm that now has to route through SMS-sending
   and log-appending code just to check a threshold comparison.

Four or five places to touch, a growing constructor signature, and every
reaction is now entangled with every other reaction inside one function --
you cannot test the alarm logic without also exercising the console print
and the log append.

**The smell:** rigidity. `set_temperature` cannot gain or lose a reaction
without being edited and recompiled, and every reaction depends on being
listed inside the same function body as every other reaction.

**The fix:** Observer lets a subject broadcast changes to a set of listeners
that register themselves at runtime. The subject holds non-owning pointers
to its observers and calls a virtual hook on each one whenever its state
changes. Adding SMS alerts becomes writing one new `Observer` subclass and
attaching an instance of it -- `Thermometer` itself never changes again.

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

Use Observer when one object's changes must reach an open-ended,
runtime-varying set of dependents -- event systems, model/view updates,
alarms.

### Template Method -- from `legacy/report_v1.cpp`

`make_sales_report()` and `make_inventory_report()` are two free functions,
each building a report by concatenating strings. `make_inventory_report()`
was copy-pasted from `make_sales_report()` to save time. Later, someone
noticed the footer had a typo -- `"--- End of Reprot ---"` -- and fixed it in
`make_sales_report()`. Nobody thought to check the copy: `make_inventory_
report()` still emits the misspelled footer today. Go look; the bug is
really there in `assets/legacy/report_v1.cpp`, sitting unnoticed because the
two functions are never compared side by side.

Now suppose the next request arrives: add a third report type, `SummaryReport`.
Doing it the way the file has always been extended means:

1. Copy one of the two existing functions wholesale.
2. Change the header and body lines for the new report.
3. Hope you copied the (correct) footer and not the misspelled one -- there
   is no single place a reviewer can check the footer is right in all three.
4. Repeat steps 1-3 for every report type added after that.

**The smell:** copy-paste divergence. Shared logic (the footer, and the
overall header-then-body-then-footer shape) exists in multiple physical
copies that are free to drift apart, and already have.

**The fix:** Template Method fixes the outline of an algorithm in a base
class and lets subclasses fill in specific steps. The base class defines a
non-virtual method that calls virtual hooks in a fixed order; the footer is
written exactly once, in the base class, so it cannot desync between report
types ever again. This is the "Hollywood principle": don't call us, we'll
call you -- the base class calls the subclass's hooks, not the other way
around.

```
        ReportGenerator::generate()   (fixed skeleton, not overridden)
              |
              +--> header()   (virtual hook -- subclass fills in)
              +--> body()     (virtual hook -- subclass fills in)
              +--> footer()   (shared, defined once in the base)
```

Use Template Method when several variants share an overall procedure but
differ in a few steps -- report formats, parsers, game turn loops.

---

## Examples at a glance

Three parts, three small domains. Each table below picks one concrete
scenario and shows what every function/method in that part produces for
it -- read these before Task if the prose above still feels abstract.

### Part 1 -- Strategy, on `v = {-3, 5, -1, 3, 2}`

| Call | Returns | Why |
|------|---------|-----|
| `Ascending().before(-3, 5)` | `true` | `-3 < 5` |
| `Ascending().before(5, -3)` | `false` | `5 < -3` is false |
| `sort_with(v, Ascending())` | `{-3, -1, 2, 3, 5}` | plain increasing order |
| `sort_with(v, Descending())` | `{5, 3, 2, -1, -3}` | plain decreasing order |
| `ByAbsoluteValue().before(-3, 2)` | `false` | `abs(-3)=3` is not `< abs(2)=2` |
| `ByAbsoluteValue().before(-3, 3)` | `true` | equal magnitude (`3 == 3`), so the tie-break `-3 < 3` decides it |
| `sort_with(v, ByAbsoluteValue())` | `{-1, 2, -3, 3, 5}` | magnitudes `1, 2, 3, 3, 5`; the two magnitude-3 values (`-3` and `3`) keep ascending order between themselves |

### Part 2 -- Observer, `HighAlarm(90)` and `TemperatureLog` both attached, readings `70, 95, 90` in that order

| Call | Returns | Why |
|------|---------|-----|
| `alarm.count()` after all three readings | `1` | only `95` is **strictly greater than** `90`; `70` and `90` itself do not count |
| `log.values()` after all three readings | `{70, 95, 90}` | every reading is recorded, in the order it arrived |
| `t.detach(&alarm)` then `t.set_temperature(200)` | `alarm.count()` stays `1`; `log.values()` becomes `{70, 95, 90, 200}` | detaching truly stops future notifications to `alarm`, but does not affect `log`, which was never detached |
| `t.detach(&alarm)` a second time | nothing happens, no crash | detaching something not currently attached is a documented no-op |

### Part 3 -- Template Method, no input (the reports are fixed data)

| Call | Returns | Why |
|------|---------|-----|
| `SalesReport().generate()` | `"=== Sales Report ===\nTotal Sales: $1000\n--- End of Report ---\n"` | `header() + body() + footer()`, in that order |
| `InventoryReport().generate()` | `"=== Inventory Report ===\nItems In Stock: 42\n--- End of Report ---\n"` | same skeleton, different hooks |
| Do `SalesReport` and `InventoryReport` footers ever disagree? | No, structurally impossible | `footer()` is written exactly once, in the base class, and neither subclass overrides it |

## Worked example: watch `ByAbsoluteValue` sort `{-3, 5, -1, 3, 2}`, step by step

This is the trickiest comparison in the assignment (the equal-magnitude
tie-break), so here is the whole insertion sort traced by hand. The
reference `sort_with` is an insertion sort: for each index `i` from `1`
upward, it holds `key = v[i]` and shifts every preceding element that
`strategy.before(key, v[j-1])` says should come after `key` one slot to
the right, then drops `key` into the gap it opened. Every single
comparison in the trace below is a call to `ByAbsoluteValue::before`,
never a raw `<` on the ints themselves.

Recall `ByAbsoluteValue().before(a, b)` compares `abs(a)` to `abs(b)`
first; only when those magnitudes are EQUAL does it fall back to
comparing `a` and `b` directly (ascending).

| `i` | `key` | shifts (each one a `before` call) | array after this `i` |
|-----|-------|-------------------------------------|-----------------------|
| 1 | `5` | `before(5, -3)`: `abs(5)=5 < abs(-3)=3`? No -> no shift | `{-3, 5, -1, 3, 2}` |
| 2 | `-1` | `before(-1, 5)`: `1 < 5`? Yes -> shift `5` right. `before(-1, -3)`: `1 < 3`? Yes -> shift `-3` right. Gap now at index 0. | `{-1, -3, 5, 3, 2}` |
| 3 | `3` | `before(3, 5)`: `3 < 5`? Yes -> shift `5` right. `before(3, -3)`: `abs(3)=3 < abs(-3)=3`? Magnitudes tie, fall back to `3 < -3`? No -> stop. | `{-1, -3, 3, 5, 2}` |
| 4 | `2` | `before(2, 5)`: `2 < 5`? Yes -> shift `5` right. `before(2, 3)`: `2 < 3`? Yes -> shift `3` right. `before(2, -3)`: `2 < 3`? Yes -> shift `-3` right. `before(2, -1)`: `2 < 1`? No -> stop. | `{-1, 2, -3, 3, 5}` |

Final array: **`{-1, 2, -3, 3, 5}`**. Check the magnitudes in that
order: `1, 2, 3, 3, 5` -- correctly non-decreasing. And the one tie
(`-3` and `3`, both magnitude `3`) landed with `-3` before `3`, exactly
as the tie-break rule ("break the tie by actual ascending value")
requires. Notice this is precisely the case that a careless copy of
"smaller magnitude first" with `>=` instead of `>` (or a forgotten
tie-break) would get wrong -- which is exactly the kind of bug Strategy
is meant to make easy to isolate and test in one small class, instead of
buried inside a bigger sort function.

---

## Task

Read the corresponding `assets/legacy/` file for each part first, then
implement the refactored target API below. Each part lives in its own
header. Implement every member function and free function declared in that
header, inside the same header file.

### Part 1 -- Strategy (`sort_strategy.hpp`)

`SortStrategy` is an abstract base class with one pure-virtual method:

```cpp
virtual bool before(int a, int b) const = 0;
```

`before(a, b)` returns `true` when `a` should be ordered before `b`. Implement
three concrete strategies:

- `Ascending` -- `before(a, b)` is `a < b`.
  *Example:* `Ascending().before(2, 5) == true`; `Ascending().before(5, 2) ==
  false`; `Ascending().before(3, 3) == false` (equal values are never
  "before" each other).
- `Descending` -- `before(a, b)` is `a > b`.
  *Example:* `Descending().before(5, 2) == true`; `Descending().before(2, 5)
  == false`; `Descending().before(3, 3) == false`.
- `ByAbsoluteValue` -- orders by absolute value, smaller magnitude first. When
  two values have equal absolute value (for example `-3` and `3`), break the tie
  by actual ascending value, so `-3` comes before `3`.
  *Example:* `ByAbsoluteValue().before(2, -3) == true` (`abs(2)=2 <
  abs(-3)=3`); `ByAbsoluteValue().before(-3, 2) == false`; `ByAbsoluteValue()
  .before(-3, 3) == true` (magnitudes tie at `3`, so it falls back to
  `-3 < 3`); `ByAbsoluteValue().before(3, -3) == false` (same tie, other
  direction).

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
*Example:* `sort_with({3, 1, 2, -5, 4}, Ascending())` sorts the vector to
`{-5, 1, 2, 3, 4}`; `sort_with({3, -3, 1, -2}, ByAbsoluteValue())` sorts it
to `{1, -2, -3, 3}` (magnitudes `1, 2, 3, 3`, tie broken ascending); an
empty vector, `sort_with({}, Ascending())`, leaves it `{}` -- there is
nothing to shift.

### Part 2 -- Observer (`thermometer.hpp`)

`Observer` is an abstract base class:

```cpp
virtual void on_temperature(double temp) = 0;
```

`Thermometer` is the subject. Implement:

- `void attach(Observer* o)` -- registers `o` for future notifications. `o` is a
  non-owning pointer; the thermometer never allocates or frees it.
  *Example:* after `t.attach(&alarm)`, the next `t.set_temperature(...)`
  call reaches `alarm.on_temperature(...)`; before any `attach`, a
  `Thermometer` with zero observers simply notifies no one.
- `void detach(Observer* o)` -- removes `o` so it receives no further
  notifications. Does nothing if `o` was never attached.
  *Example:* `t.attach(&alarm); t.detach(&alarm);` then
  `t.set_temperature(500)` leaves `alarm.count() == 0` -- it was removed
  before the reading arrived; calling `t.detach(&alarm)` a second time (or
  on an observer that was never attached at all) does nothing and does not
  crash.
- `void set_temperature(double temp)` -- calls `on_temperature(temp)` on every
  attached observer, in the order they were attached.
  *Example:* with `alarm` attached before `log`, `t.set_temperature(70)`
  calls `alarm.on_temperature(70)` first, then `log.on_temperature(70)`;
  with zero observers attached, `set_temperature` does nothing observable
  at all.

Implement two concrete observers:

- `HighAlarm(double threshold)` -- `count()` returns how many notified
  temperatures were **strictly greater than** `threshold`. A value equal to the
  threshold does not count.
  *Example:* `HighAlarm alarm(100.0);` then notifying `50.0`, `150.0`,
  `200.0` in turn leaves `alarm.count() == 2`; notifying exactly `100.0`
  (equal to the threshold) leaves `count()` unchanged -- it does not count;
  a `HighAlarm` that has never been notified has `count() == 0`.
- `TemperatureLog` -- records every notified temperature in order; `values()`
  returns them as a `const std::vector<double>&`.
  *Example:* notifying `1.0`, `2.0`, `3.0` in turn leaves
  `log.values() == std::vector<double>{1.0, 2.0, 3.0}`; a fresh
  `TemperatureLog` that has never been notified has `values() == {}`
  (empty).

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
  *Example:* `SalesReport().generate() ==
  "=== Sales Report ===\nTotal Sales: $1000\n--- End of Report ---\n"`;
  `InventoryReport().generate() ==
  "=== Inventory Report ===\nItems In Stock: 42\n--- End of Report ---\n"`;
  both share the exact same trailing `"--- End of Report ---\n"`, because
  `footer()` is defined once, in the base class, and neither subclass
  overrides it.

So `SalesReport().generate()` returns exactly:

```
=== Sales Report ===
Total Sales: $1000
--- End of Report ---
```

Note that this base-class footer is exactly the fix for the desync bug in
`legacy/report_v1.cpp`: because it is written once, `SalesReport` and
`InventoryReport` cannot disagree about how a report ends.

The hidden tests compare `generate()` output byte for byte, so reproduce the
strings, including the trailing newlines, precisely.

## Files

| File | Purpose |
|------|---------|
| `sort_strategy.hpp` | Part 1 -- Strategy; edit and implement here |
| `thermometer.hpp` | Part 2 -- Observer; edit and implement here |
| `report_generator.hpp` | Part 3 -- Template Method; edit and implement here |
| `legacy/sort_modes.cpp` | Reference only -- read, do not modify or submit |
| `legacy/thermometer_v1.cpp` | Reference only -- read, do not modify or submit |
| `legacy/report_v1.cpp` | Reference only -- read, do not modify or submit |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
cd visible-tests
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

- Refactor `legacy/sort_modes.cpp`, `legacy/thermometer_v1.cpp`, and
  `legacy/report_v1.cpp` yourself, end to end, into the Strategy/Observer/
  Template Method shapes -- then diff your refactor against your
  `pattern-toolkit` implementation. How close are they?
- Find the desync bug in `legacy/report_v1.cpp` before reading the Template
  Method section above, and explain in one sentence why the base-class
  `footer()` in `report_generator.hpp` makes that bug structurally
  impossible to reintroduce.
- Add a `ByLastDigit` strategy that orders ints by their least-significant
  decimal digit and pass it to `sort_with`. Notice you changed no sort code.
- Add a `RangeAlarm(double low, double high)` observer that counts
  temperatures falling inside a band, attach it alongside `HighAlarm`, and
  confirm both fire on the same `set_temperature` call.
- Read about the open-closed principle (open for extension, closed for
  modification) and identify which part of each legacy file violated it.
