# Lazy Pipeline

yield-yard proved that a generator pauses and resumes -- and that a
generator expression's side effects happen on consumption, not creation.
This assignment turns that idea into a real tool: a small log-processing
pipeline built entirely out of generator functions, chained one into the
next. The graded contract is not just "does it produce the right
values" -- it is "does it produce them **lazily**." A function that
secretly builds a full list before yielding anything passes a naive
correctness check but fails this assignment's hidden tests, which watch
*how much of the input was actually touched*, not just what came out the
other end.

## Learning goals

- Write a chain of generator functions, each consuming exactly as much
  of its input as its own caller demands
- Use `Iterable` and `Iterator` type hints to describe generator-based
  APIs (tying directly back to Annotation Arsenal and TypeVar Tracer)
- Distinguish "produces the right values" from "produces them lazily" --
  and understand why the second property matters for a source that is
  very large, or effectively unbounded
- Practice generator exhaustion (one-shot) semantics: a generator that
  has already been fully consumed yields nothing on a second pass
- Handle malformed input and boundary conditions (empty input, `n = 0`,
  a final partial chunk) without breaking laziness

## Examples at a glance

To make all five functions concrete, here is **one** representative pipeline
of raw log lines, and what each stage produces from it. Read this table
first -- it is the whole assignment in miniature.

```
lines = [
    "INFO:one", "ERROR:bad", "INFO:two", "garbage",
    "INFO:three", "ERROR:worse", "INFO:four", "INFO:five",
]
```

("garbage" has no colon in it at all, so it is malformed.)

| Call | Returns | Why |
|------|---------|-----|
| `list(parse_records(lines))` | `[{"level": "INFO", "msg": "one"}, {"level": "ERROR", "msg": "bad"}, {"level": "INFO", "msg": "two"}, {"level": "INFO", "msg": "three"}, {"level": "ERROR", "msg": "worse"}, {"level": "INFO", "msg": "four"}, {"level": "INFO", "msg": "five"}]` | every well-formed `"LEVEL:msg"` line becomes a dict; `"garbage"` has no colon, so it is silently skipped -- it produces nothing at all, not an error |
| `list(only_level(parse_records(lines), "INFO"))` | `[{"level": "INFO", "msg": "one"}, {"level": "INFO", "msg": "two"}, {"level": "INFO", "msg": "three"}, {"level": "INFO", "msg": "four"}, {"level": "INFO", "msg": "five"}]` | keeps only the records whose level is exactly `"INFO"`, in the same order they arrived |
| `list(take(only_level(parse_records(lines), "INFO"), 3))` | `[{"level": "INFO", "msg": "one"}, {"level": "INFO", "msg": "two"}, {"level": "INFO", "msg": "three"}]` | stops after the 3rd matching `INFO` record -- notice this is the *first three INFO records*, not the first three lines |
| `list(running_count(only_level(parse_records(lines), "INFO")))` | `[1, 2, 3, 4, 5]` | one number per `INFO` record actually seen, counting up from 1 |
| `list(chunked(list(only_level(parse_records(lines), "INFO")), 2))` | `[[{"level": "INFO", "msg": "one"}, {"level": "INFO", "msg": "two"}], [{"level": "INFO", "msg": "three"}, {"level": "INFO", "msg": "four"}], [{"level": "INFO", "msg": "five"}]]` | groups the 5 `INFO` records into chunks of 2; since 5 is not a multiple of 2, the last chunk has only 1 item -- it is still yielded, not dropped |

**The `take(..., 3)` row is the important one:** it stops at the 3rd
`INFO` record, which is `"INFO:three"` -- the 4th and 5th line's worth
of `INFO` records (`"INFO:four"`, `"INFO:five"`), and everything after
them, are **never even read**. The next section walks through exactly
why.

## Worked example: watch the pipeline pull one item at a time

This is the single most important thing to understand in the assignment: a
chain of generators does not compute anything up front. Each stage only
asks the stage before it for one more item at the exact moment its own
caller asks *it* for one more item. Here is that chain, called on
`lines` from above:

```python
records = parse_records(lines)
info_only = only_level(records, "INFO")
limited = take(info_only, 3)
result = list(limited)
```

`list(limited)` repeatedly asks `limited` (the `take` generator) for "one
more item" until it says "no more." Here is what happens on every single
one of those asks, and which raw lines get touched to answer it:

| Ask # | What `take` does | What that forces `only_level` to do | What that forces `parse_records` to do | Item produced |
|-------|-------------------|--------------------------------------|-------------------------------------------|----------------|
| 1 | `count = 0 < 3`, pulls one item from `info_only` | pulls one record from `records` | pulls `lines[0] = "INFO:one"`, parses it, yields `{"level": "INFO", "msg": "one"}` | `only_level` sees level `"INFO"` matches, yields it; `take` yields it, `count = 1` |
| 2 | `count = 1 < 3`, pulls again | pulls one record; gets `"ERROR"`, does NOT match, pulls again | pulls `lines[1] = "ERROR:bad"` (yielded, since it's well-formed), then pulls `lines[2] = "INFO:two"` | `only_level` yields `{"level": "INFO", "msg": "two"}`; `take` yields it, `count = 2` |
| 3 | `count = 2 < 3`, pulls again | pulls one record; gets `"INFO"`, matches | pulls `lines[3] = "garbage"` -- no colon, skipped silently, so `parse_records` immediately pulls `lines[4] = "INFO:three"` instead and yields it | `only_level` yields `{"level": "INFO", "msg": "three"}`; `take` yields it, `count = 3` |
| 4 | `count = 3 >= 3` already, so `take` returns (stops) WITHOUT pulling anything from `info_only` | (not called) | (not called) | none -- `take` is exhausted, `list()` stops |

`result` ends up `[{"level": "INFO", "msg": "one"}, {"level": "INFO",
"msg": "two"}, {"level": "INFO", "msg": "three"}]` -- exactly the
`take(..., 3)` row from the table above.

**Notice `lines[5] = "ERROR:worse"`, `lines[6] = "INFO:four"`, and
`lines[7] = "INFO:five"` are never touched at all** -- not parsed, not
filtered, not looked at in any way. `parse_records` never even calls
`next()` on `lines` a 6th time, because nothing downstream ever asked
for a 6th item. If `lines` were reading from a multi-gigabyte log file
instead of a Python list, this chain would only ever read the first five
lines of that file to produce these three results -- **the rest of the
file would sit on disk, untouched.** That is what "lazy" means in this
assignment's grading: not just correct output, but a source that is
pulled from exactly as many times as necessary and no more.

## Task

Implement five functions in a file named `pipeline.py`, each a generator
function (uses `yield`, not `return`, to produce its values).

### `parse_records`

```python
def parse_records(lines: Iterable[str]) -> Iterator[dict[str, str]]:
```

**Each line is formatted `"LEVEL:message"`.** For each well-formed line,
lazily yield `{"level": LEVEL, "msg": message}` (the level has any
surrounding whitespace stripped; the message is kept exactly as-is,
including any additional colons it may contain). A line with no colon
at all, or with an empty level before the first colon, is malformed --
skip it silently rather than yielding anything for it. Do not read
ahead: only pull the next line from `lines` when a caller actually asks
`parse_records` for another record.

*More examples:*
- **Empty input:** `list(parse_records([])) == []` -- the `for` loop
  over `lines` simply **never runs**.
- **Edge case (empty level):** `list(parse_records([":no level"])) ==
  []` -- the text before the first colon is empty (nothing to strip),
  so this line is **malformed and skipped**, just like a line with no
  colon at all.
- **Tricky case (extra colons):** `list(parse_records(["INFO:time is
  10:30:00"])) == [{"level": "INFO", "msg": "time is 10:30:00"}]` --
  only the **first colon** splits level from message; every colon after
  that stays part of `msg` untouched.

### `only_level`

```python
def only_level(records: Iterable[dict[str, str]], level: str) -> Iterator[dict[str, str]]:
```

**Lazily yield only the records whose `"level"` value equals `level`
exactly**, preserving order.

*More examples:*
- **Empty input:** `list(only_level([], "INFO")) == []`.
- **Tricky case (case sensitivity):** `list(only_level([{"level":
  "INFO", "msg": "a"}], "info")) == []` -- the comparison is **exact and
  case-sensitive**: `"info"` does not match `"INFO"`.
- **Example (single match):** `list(only_level([{"level": "ERROR",
  "msg": "x"}], "ERROR")) == [{"level": "ERROR", "msg": "x"}]` -- **a
  matching record is kept**.

### `take`

```python
def take(iterable: Iterable, n: int) -> Iterator:
```

**Yield at most `n` items from `iterable`, in order, then stop -- and
consume no more than `n` items from `iterable` to get them.** This is
the laziness proof hook for the whole assignment: `take` must never pull
an `n + 1`th item from its source just to check whether there is one.
If `n <= 0`, yield nothing and touch nothing.

*More examples:*
- **Example (source runs out early):** `list(take([1, 2], 5)) == [1,
  2]` -- asking for more than the source has is fine; `take` stops as
  soon as the source runs out (**never errors** for asking too much).
- **Edge case (`n = 0`):** `list(take([1, 2, 3], 0)) == []` -- `take`
  returns immediately without pulling **a single item** from `[1, 2,
  3]` (zero items requested, zero items touched).
- **Example (exact pull count):** `list(take([1, 2, 3, 4, 5], 3)) ==
  [1, 2, 3]` -- with an instrumented source that logs every pull, only
  **three pulls** would be logged here, never a fourth "just to check"
  whether more remain.

### `running_count`

```python
def running_count(records: Iterable[dict[str, str]]) -> Iterator[int]:
```

**For each record pulled from `records`, in order, yield the number of
records seen so far** (starting at 1 for the first one).

*More examples:*
- **Empty input:** `list(running_count([])) == []` -- nothing was ever
  seen, so **nothing is yielded** (not even a `0`).
- **Example (single record):** `list(running_count([{"level": "INFO",
  "msg": "a"}])) == [1]`.
- **Example (chained after `take`):** `list(running_count(take([{"level":
  "INFO", "msg": "a"}] * 10, 2))) == [1, 2]` -- `running_count` only ever
  sees the **2 records `take` lets through**, so it only ever counts up
  to `2`, never higher.

### `chunked`

```python
def chunked(iterable: Iterable, size: int) -> Iterator[list]:
```

**Yield successive lists of up to `size` items pulled from `iterable`.**
If the number of items is not an exact multiple of `size`, the final,
shorter chunk is still yielded (not dropped). `size` must be a positive
integer.

*More examples:*
- **Empty input:** `list(chunked([], 3)) == []` -- produces **no
  chunks at all**, not a single empty chunk.
- **Example (`size` bigger than input):** `list(chunked([1, 2], 5)) ==
  [[1, 2]]` -- everything just becomes **one (short) chunk**.
- **Tricky case (invalid `size`, lazy raise):** `chunked([1, 2], 0)`
  does **not raise** the moment you call it -- like every function here,
  `chunked` is a generator, so nothing runs until you ask it for a first
  item; only calling `next()` on it (for example, via `list(...)`)
  actually raises `ValueError`.

### Examples

```python
>>> list(parse_records(["INFO:started", "garbage", "ERROR:boom"]))
[{'level': 'INFO', 'msg': 'started'}, {'level': 'ERROR', 'msg': 'boom'}]
>>> list(only_level([{"level": "INFO", "msg": "a"}, {"level": "ERROR", "msg": "b"}], "INFO"))
[{'level': 'INFO', 'msg': 'a'}]
>>> list(take([1, 2, 3, 4, 5], 3))
[1, 2, 3]
>>> list(running_count([{"level": "INFO", "msg": "a"}] * 3))
[1, 2, 3]
>>> list(chunked([1, 2, 3, 4, 5], 2))
[[1, 2], [3, 4], [5]]
```

Chained together, a small pipeline looks like this:

```python
records = parse_records(log_lines)
errors_only = only_level(records, "ERROR")
first_five_errors = list(take(errors_only, 5))
```

If `log_lines` were a generator reading from an enormous file, this
chain would only ever read as far into the file as needed to find five
`ERROR` records -- not the whole file.

## Files

| File | Purpose |
|------|---------|
| `pipeline.py` | Write your implementation here |

## Compilation and Testing

```bash
python -m pytest visible-tests/test_visible.py -v
```

## Constraints

- Do not rename `pipeline.py`, or rename/remove any function.
- Type hints are required on every function's parameters and return type
  (`Iterable`/`Iterator` from `typing`, matching the signatures above).
- `pipeline.py` must not import `itertools` -- write every stage's
  pause/resume logic yourself rather than reaching for
  `itertools.islice`, `itertools.chain`, or similar to do it for you.
- **Type-annotation bonus (10 pts):** every function must annotate all of
  its parameters and its return type (the `Iterable`/`Iterator` signatures
  above). The bonus is awarded only when every function is fully annotated;
  a separate, informational [ty](https://docs.astral.sh/ty/) check then flags
  any annotation that does not hold up.

## Grading

| Component                           | Points |
|--------------------------------------|--------|
| Import constraints (gate)            | 5      |
| Visible correctness tests            | 35     |
| Hidden correctness tests             | 50     |
| Complete type annotations (bonus)    | 10     |
| **Total**                            | **100** |

Hidden tests cover: laziness (an instrumented source proves `take`
consumes no more than requested), malformed-line skipping, `chunked`'s
exact-multiple and partial-tail boundaries, empty input, `n = 0`, and
generator one-shot semantics (an exhausted generator yields nothing on a
second pass).

## Submission

Submit your implementation as `pipeline.py`. Do not rename it.

## Going further

- Rewrite `take` using `itertools.islice` (outside this assignment's own
  constraints) and compare the two implementations. What does
  `itertools` buy you, and what did you learn by writing it by hand
  first?
- Add a `peek(iterable)` generator that yields every item unchanged but
  also prints it as a side effect -- insert it into a pipeline chain and
  observe exactly when each print happens relative to `take`'s bound.
- What would have to change about `parse_records` if a single logical
  record could span multiple lines (a multi-line stack trace, say)? Is
  that still expressible as a simple generator function?
