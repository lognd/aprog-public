# Study Guide 53: Python Generics & Typing

This module reads and chooses Python type annotations (generic
containers, `Optional`/`|None`, `Callable[[...], R]`, `TypeVar` vs.
`@overload`) and then proves by running code that none of it has any
runtime effect -- annotations are inspectable data for a static checker,
never enforced by the interpreter.

## Know before you start

- `template<typename T>` as the C++ analogue for a `TypeVar` [assumed:
  row 23 -- Polymorphism]
- `const` as the C++ analogue for the enforcement contrast [assumed: row
  13 -- Const]
- Type annotations existing as unenforced documentation [assumed: row 52
  -- Python Types & Comprehensions]
- Mutable default arguments requiring the general mutable-vs-immutable
  distinction [assumed: row 47 -- Python Data Types]

## Taught here

Concept: reading and choosing annotations
- Know generic container annotations: `list[int]`, `dict[str, int]`,
  `tuple[int, ...]` (variable-length homogeneous tuple), and nested forms
  like `list[list[int]]`.
- Know `Optional[X]` (or its Python 3.10+ equivalent, `X | None`) marks a
  value that may be `X` or may be `None`.
- Be able to read a `Callable[[ParamTypes], ReturnType]` signature
  describing a function value's parameter and return types.
- Know `TypeVar` is Python's closest analogue to a C++ function template
  parameter: a single `TypeVar` used in both a parameter and a return
  type expresses one relationship holding for every possible type at
  once.
- Know `@overload` is closer to C++ overloading: it requires one
  hand-written signature per case, and any case not written gets no
  static-checking benefit.
- Know `Any` is a deliberate, honest tradeoff (opts a value out of static
  checking entirely), not a free win.
- Know a static type checker (`ty`, `mypy`) reports a mismatched call as
  a SEPARATE analysis pass over the source, entirely apart from actually
  running the code.

Concept: annotations have zero runtime effect
- Know `__annotations__` is an ordinary, inspectable dictionary stored on
  a function object -- data that exists, but that nothing in Python's own
  call machinery ever consults while the function actually runs.
- Know an annotated parameter cheerfully accepts a mismatched value (e.g.
  a string where `int` was annotated) with no coercion, no error, and no
  special behavior at call time.
- Know deleting every annotation and every `TypeVar` from a generic
  function changes zero bytecode and produces exactly the same results --
  `TypeVar`'s entire job is to give a static checker something to reason
  about.
- Know `get_type_hints` resolves a string-form annotation into the real
  type object it names, still purely for inspection, never for
  enforcement.
- Be able to use `isinstance` against a Python 3.10+ union written with
  `|`.

Concept: the local quality toolbox (linter, formatter, type checker)
- Know each tool's job: `ruff check` is a linter (flags legal-but-
  almost-certainly-wrong patterns like unused imports, undefined names,
  mutable default arguments), `ruff format` is a formatter (rewrites
  layout to one canonical style, never behavior), `ty` is a static type
  checker (reads the annotations the interpreter ignores and reports
  broken promises without running the code), and `pytest` runs the
  tests. `mypy` and `black` are the classic equivalents of `ty` and
  `ruff format`.
- Know the fix loop discipline: run the tool, read the FIRST error,
  fix the smallest thing it points at, rerun.
- Know a type checker catches paths tests never exercise (a function
  that can implicitly return `None` fails `ty` even when every test
  passes), and that tools can overlap: one typo can show up as a ruff
  F821 and a ty unresolved-reference at once.

Concept: pytest in depth
- Know discovery is naming: pytest collects `test_*.py` files and
  `test_*` functions; `pytest --collect-only -q` lists what it found,
  one node ID per line.
- Know plain `assert` failures show both sides of the comparison
  (pytest rewrites asserts for introspection -- no REQUIRE macro
  needed).
- Know `@pytest.mark.parametrize` runs one test body once per case,
  each case its own node ID, failures reported individually.
- Know fixtures are injected by parameter name (`tmp_path` gives a
  fresh temporary directory; `monkeypatch` temporarily replaces
  attributes or environment variables and undoes itself).
- Be able to assert an expected exception with
  `pytest.raises(ValueError)`.
- Know markers (`@pytest.mark.slow`, registered in pyproject.toml) and
  selection: `-m "not slow"` deselects by marker, `-k name` selects by
  name substring.
- Know a coverage percentage means lines EXECUTED by tests, not
  correctness -- an assert-free suite can score 100%.

Concept: CI/CD, secrets, and .env practices
- Know CONTINUOUS INTEGRATION means a robot runs the project's checks
  on every push, and CONTINUOUS DEPLOYMENT adds automated shipping
  after the checks pass -- on top of CI, never instead of it.
- Know GitHub Actions workflow anatomy: the `on:` trigger says WHEN
  (push, pull_request, tags), each job is a fresh virtual machine, and
  commands like `uv run pytest` are steps inside a job.
- Know the red X blocking a merge is a feature: it moves "remember to
  run the checks" out of human memory into a mechanism.
- Know "passes locally, fails in CI" usually means version or
  environment drift, fixed by installing from a committed lockfile
  (`uv.lock`, `uv sync --locked`).
- Know credentials live in GitHub Actions Secrets, never in the repo:
  the runner masks secret values in logs, fork PRs run without
  secrets, and environment secrets can require manual approval before
  a production job runs.
- Know the ssh deploy skeleton (authenticate via ssh-agent +
  ssh-keyscan, rsync the artifacts, restart the service over ssh) and
  the deploy-trigger tradeoff (push-to-main ships every merge;
  tag/release keeps a human decision in the loop).
- Know the .env pattern: real values in a gitignored `.env` read by
  `load_dotenv()` at runtime, variable NAMES documented in a committed
  `.env.example` with fake values, and code reading `os.environ`
  identically in every environment.

Concept: the mutable-default-argument trap
- Know `def f(xs: list[int] = []):` builds that empty list object exactly
  ONCE, at the moment `f` is DEFINED -- not fresh on every call that omits
  `xs` -- so every call sharing the default shares and mutates the SAME
  list object.
- Know `is` (not `==`) is the way to confirm two default-argument results
  from separate calls are literally the same object, since two lists can
  look identical when printed while still being different objects.
- Be able to fix the trap with the `xs: list[int] | None = None` idiom,
  building a fresh list inside the function body when `xs is None`.

## Study checklist

- [ ] Pick the correct annotation (list[int], dict[str,int], Optional/|
      None, Callable[[...],R]) for a described value.
- [ ] Explain the TypeVar-vs-overload distinction using the C++
      template-vs-overload analogy.
- [ ] Explain why an int-annotated parameter can hold a string at
      runtime with no error.
- [ ] Predict output of two calls sharing a mutable default argument.
- [ ] Fix a mutable-default trap using the None-default idiom.
- [ ] Explain what a static checker does that the interpreter does not.

## Practiced in

`annotation-arsenal`, `typevar-tracer`, `make-the-linter-happy`,
`pytest-dojo`, `ship-it-pipeline`
