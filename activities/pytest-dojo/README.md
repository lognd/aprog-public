# Activity: Pytest Dojo

pytest is the tool that has been grading you this whole course. Every
Python assignment you have submitted was checked by a pytest suite the
instructors wrote -- and in the make-the-linter-happy activity, pytest
was the fourth gate. So far you have only ever been on the receiving
end. In this activity you switch sides: you get a small, working module
and an almost-empty test file, and you write the tests.

You already met these ideas in C++ costume back in the testing-tools
module (row 17): Catch2's `TEST_CASE` is pytest's test function,
`REQUIRE` is pytest's plain `assert`, and tags with `[brackets]` are
pytest's markers. Same concepts, new (much lighter) syntax.

## Concepts covered

- Test discovery: which files and functions pytest runs, and why naming
  is the whole mechanism
- Plain `assert` plus pytest's failure introspection
- `@pytest.mark.parametrize`: one test body, many cases
- Fixtures (`tmp_path`), and `pytest.raises` for expected exceptions
- Markers and test selection with `-m` and `-k`

## Background

Everything below is exercised in the shell; skim it now, come back as
you write each test.

**Discovery.** pytest never asks you for a list of tests. It walks the
directory looking for files named `test_*.py` (or `*_test.py`), and
inside them collects every function whose name starts with `test_`.
That is the entire registration mechanism -- a test you forgot to name
`test_...` silently does not exist. `pytest --collect-only -q` shows
you exactly what pytest found, one NODE ID per line:

```
tests/test_phrasebook.py::test_shout_adds_emphasis
^ file                     ^ function
```

**Plain assert.** Where Catch2 needed the `REQUIRE` macro, pytest
rewrites ordinary `assert` statements at import time so that a failure
shows the values on both sides, not just "AssertionError":

```
>       assert shout("hola") == "HOLA"
E       AssertionError: assert 'HOLA!' == 'HOLA'
```

The actual value is on the left, your expectation on the right. When a
test fails, one of those two is lying; read both before touching code.

**Parametrize.** `@pytest.mark.parametrize` runs one test body once per
case, and each case becomes its own node ID:

```python
@pytest.mark.parametrize(("phrase", "expected"), [
    ("hello", "hola"),
    ("goodbye", "adios"),
])
def test_translate_pairs(phrase, expected):
    assert translate(phrase) == expected
```

collects as `test_translate_pairs[hello-hola]` and
`test_translate_pairs[goodbye-adios]` -- two tests, one body. Failing
cases are reported individually, which is why this beats a for-loop
inside one test (a loop stops at the first failing iteration and hides
the rest).

**Fixtures.** A FIXTURE is a named piece of setup that pytest injects
into your test when the test asks for it by parameter name. Write
`def test_x(tmp_path):` and pytest hands you `tmp_path`, a freshly
created temporary directory (as a `pathlib.Path`), unique to this test
run and cleaned up for you. No registration, no boilerplate -- the
parameter NAME is the request. `tmp_path` is built in; so are many
others (`capsys` captures printed output, for example).

One more built-in worth knowing now: `monkeypatch` temporarily replaces
an attribute, environment variable, or dictionary entry for the
duration of one test, and undoes the change automatically afterward --
`monkeypatch.setenv("HOME", str(tmp_path))`, for example, lets a test
control what `os.environ` says without polluting the real environment.
You will not need it in this activity, but it is the standard answer to
"how do I test code that reads global state?"

**Expected exceptions.** When bad input is SUPPOSED to raise, assert
that it does:

```python
with pytest.raises(ValueError):
    translate("flibbertigibbet")
```

The test fails if the block does NOT raise `ValueError`. This is the
error-path twin of a normal assertion -- untested error paths are where
bugs retire and live comfortably.

**Markers and selection.** A MARKER is a label on a test.
`@pytest.mark.slow` tags a test as slow; the project's `pyproject.toml`
registers the name (look at it -- unregistered markers only produce a
warning, which is how typos in marker names slip through). Then `-m`
selects by marker: `pytest -m "not slow"` runs everything except
slow-marked tests, reporting them as "deselected". `-k` selects by name
substring instead: `pytest -k translate` runs only tests with
"translate" in the name. Both exist so a huge suite can give you a
fast, relevant subset while you work.

**conftest.py.** One paragraph, because you will meet it in real
projects: a file named `conftest.py` holds fixtures and hooks shared by
every test file in its directory (and below) -- define a fixture there
once and any test can request it by name, no import needed. This
project is small enough not to need one; know that the name is magic
and that "where does this fixture come from?" is usually answered
there.

## How it works

The launcher unpacks the project and drops you into a shell.
`phrasebook.py` works; `tests/test_phrasebook.py` contains one broken
test and a list of four tests that do not exist yet. You fix the broken
assertion and write the four tests. The checker finds your tests by
their exact names, so use the names given.

When you `exit`, the launcher runs pytest itself, three ways:

1. `pytest --collect-only -q` -- the required node IDs must exist, with
   `test_translate_pairs` collecting at least 3 parametrized cases
2. `pytest -q` -- the whole suite must pass
3. `pytest -m "not slow" -q` -- must pass AND deselect the slow scan

All three green unlocks the passphrase.

## Getting started

pytest must be installed (`uv tool install pytest` -- see
env-setup-python if it is missing).

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- run the suite and fix the broken test

```bash
pytest -q
```

One test fails. Read the failure report bottom-up: which assertion,
what the two values were. Decide which side is lying (check `shout()`'s
docstring) and fix the expectation.

### Step 2 -- write the four tests

In `tests/test_phrasebook.py` (you will need `import pytest` and more
names from `phrasebook`):

- `test_translate_pairs` -- parametrized over at least 3
  `(phrase, expected)` cases
- `test_translate_rejects_unknown` -- `pytest.raises(ValueError)`
  around a phrase the book does not know
- `test_phrasebook_roundtrip` -- take `tmp_path` as a parameter, save
  the phrasebook to a file inside it, load it back, assert equality
- `test_full_dictionary_scan` -- `@pytest.mark.slow`; check every entry
  in `PHRASES` translates to itself via `translate`

Rerun `pytest -q` after EACH test you write, not after all four -- the
one-failure-at-a-time loop from make-the-linter-happy applies to
writing tests too.

### Step 3 -- watch pytest see your tests

```bash
pytest --collect-only -q
```

Count the node IDs: the parametrized test appears once per case. If a
test is missing from this list, its name is wrong -- discovery is
naming.

### Step 4 -- prove the marker works

```bash
pytest -m "not slow" -q
pytest -k translate -q
```

The first should end with `1 deselected`; the second shows `-k` name
selection on the same suite, no markers involved.

### Step 5 -- exit

```bash
exit
```

The launcher collects and runs your suite itself. If something is
missing or failing, it tells you which of the three checks stopped it
and offers to drop you back in.

## You will know you are done when...

`pytest -q` passes, `pytest -m "not slow" -q` passes with the slow scan
deselected, and after you `exit`, the launcher's own three pytest runs
agree and it prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- the broken assertion</summary>

Run it and read: `assert 'HOLA!' == 'HOLA'`. The left side is what
`shout("hola")` actually returned; the docstring confirms the `!` is
intended behavior. The test's expectation is the liar here. (Sometimes
it is the code. That judgment -- which side is lying -- is the actual
skill.)

</details>

<details>
<summary>Hint 2 -- parametrize shape</summary>

The decorator takes the parameter names and a list of tuples, one tuple
per case: `@pytest.mark.parametrize(("phrase", "expected"), [(..., ...),
...])`, and the test function takes those names as parameters. Pick
your 3+ cases straight out of `PHRASES`.

</details>

<details>
<summary>Hint 3 -- tmp_path is a pathlib.Path</summary>

`tmp_path / "book.json"` builds a path inside the temporary directory;
`save_phrasebook` wants a string, so pass `str(path)`. Never write test
files into the project directory itself -- tests that scribble on the
working tree are tests that pass alone and fail together.

</details>

## Going further

These go beyond what the checker gates -- nothing here is required.

- Coverage: `uv tool install pytest-cov`, then
  `pytest --cov=phrasebook`. The percentage is the fraction of lines
  your tests EXECUTED -- honest paragraph: high coverage means your
  tests visited the code, not that they asserted anything true about
  it. A suite of tests with no asserts can score 100%. Low coverage
  reliably tells you something is untested; high coverage does not tell
  you the tests are good. Treat it as a flashlight, not a grade.
- pytest-testmon reruns only the tests affected by what you changed
  since the last run -- this course's own Makefiles use it, which is
  why a one-line fix does not rerun the whole grading suite. Try it:
  `pytest --testmon`, change one function, run again.
- The plugin ecosystem is enormous (over a thousand packages named
  `pytest-*`): `pytest-xdist` runs tests in parallel, `pytest-mock`
  wraps mocking, `pytest-asyncio` handles async tests. Browse the
  plugin list once so you know what exists before writing it yourself.
- Debugging: `pytest --pdb` drops you into Python's interactive
  debugger at the exact point a test fails, with all its variables live.
- Rewrite one of your four tests as a Catch2 `TEST_CASE` on paper.
  Which parts of the pytest version does C++ make you spell out by
  hand?
