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

## Task

Implement five functions in a file named `pipeline.py`, each a generator
function (uses `yield`, not `return`, to produce its values).

### `parse_records`

```python
def parse_records(lines: Iterable[str]) -> Iterator[dict[str, str]]:
```

Each line is formatted `"LEVEL:message"`. For each well-formed line,
lazily yield `{"level": LEVEL, "msg": message}` (the level has any
surrounding whitespace stripped; the message is kept exactly as-is,
including any additional colons it may contain). A line with no colon
at all, or with an empty level before the first colon, is malformed --
skip it silently rather than yielding anything for it. Do not read
ahead: only pull the next line from `lines` when a caller actually asks
`parse_records` for another record.

### `only_level`

```python
def only_level(records: Iterable[dict[str, str]], level: str) -> Iterator[dict[str, str]]:
```

Lazily yield only the records whose `"level"` value equals `level`
exactly, preserving order.

### `take`

```python
def take(iterable: Iterable, n: int) -> Iterator:
```

Yield at most `n` items from `iterable`, in order, then stop -- **and
consume no more than `n` items from `iterable` to get them.** This is
the laziness proof hook for the whole assignment: `take` must never pull
an `n + 1`th item from its source just to check whether there is one.
If `n <= 0`, yield nothing and touch nothing.

### `running_count`

```python
def running_count(records: Iterable[dict[str, str]]) -> Iterator[int]:
```

For each record pulled from `records`, in order, yield the number of
records seen so far (starting at 1 for the first one).

### `chunked`

```python
def chunked(iterable: Iterable, size: int) -> Iterator[list]:
```

Yield successive lists of up to `size` items pulled from `iterable`. If
the number of items is not an exact multiple of `size`, the final,
shorter chunk is still yielded (not dropped). `size` must be a positive
integer.

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
- A clean run of [ty](https://docs.astral.sh/ty/) (a fast, modern Python
  type checker, run over `pipeline.py`) earns a bonus.

## Grading

| Component                           | Points |
|--------------------------------------|--------|
| Import constraints (gate)            | 5      |
| Visible correctness tests            | 35     |
| Hidden correctness tests             | 50     |
| Clean `ty` type-check (bonus)        | 10     |
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
