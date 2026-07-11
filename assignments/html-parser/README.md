# HTML Parser

You will implement a minimal HTML parser in C++ and write a **test suite**
(a Catch2 program made up of many small `TEST_CASE`s, each checking one
behavior) that covers every **edge case** the spec describes -- an edge
case is an input at the boundary of what the spec covers (empty strings,
malformed tags, nesting) rather than a typical, easy input.  This
assignment has two graded components that are roughly equal in weight: the
correctness of your parser and the quality of your tests.  A parser that
passes the staff's hidden tests (tests the course staff wrote and kept
private, so you cannot simply write your parser to match them) but has a
thin test suite will lose points, and vice versa.

## Overview

The parser handles a 1970s-style subset of HTML: no attributes, no DOCTYPE, no
`<html>` or `<body>` tags.  Just the handful of formatting tags that were at
the core of early web content: `<b>`, `<i>`, `<u>`, `<br>`, and `<p>`.  The
two functions you implement strip tags from text and count tag occurrences.

This is also your first assignment that asks you to write the test suite
yourself.  The skills practiced here -- test organization, edge-case thinking,
and fault detection -- are the same ones you exercised in the Testing Tools
activities.

---

## Examples at a glance

To make both functions concrete, here is **one** HTML snippet, with what
`to_text` and `count_tag` each produce for it. Read this table first -- it is
the whole assignment in miniature.

```
html = "<p>Hi <b>there</b><br>friend<i>!</i>"
```

| Call | Returns | Why |
|------|---------|-----|
| `to_text(html)` | `"\n\nHi there\nfriend!"` | `<p>` opens with `\n\n`; `Hi ` passes through unchanged; `<b>`/`</b>` are stripped (no special meaning), leaving `there`; `<br>` becomes `\n`; `friend` passes through; `<i>`/`</i>` are stripped, leaving `!` |
| `count_tag(html, "p")` | `1` | one open `<p>`, no close `</p>` in this snippet |
| `count_tag(html, "b")` | `1` | only the OPEN `<b>` counts; `</b>` is a close tag and is never counted |
| `count_tag(html, "br")` | `1` | one `<br>` |
| `count_tag(html, "i")` | `1` | only the OPEN `<i>` counts; `</i>` is a close tag and is never counted |
| `count_tag(html, "u")` | `0` | `<u>` never appears in this snippet at all |

## Worked example: watch `to_text` and `count_tag("...", "b")` run, tag by tag

This is the single most important thing to understand in the assignment, so
here is every character-scanning step spelled out. The input this time
deliberately mixes a case-different tag, a `<br>`, a close tag, and a
malformed tag (one with no closing `>`) so you can see every rule fire:

```
html = "<B>Hi<br>bye</B>x<bad"
```

The scan keeps one index `i` that always points at the next unread
character. Each row below is one pass through the loop.

| `i` points at | What the scanner sees | Rule applied | Appended to `to_text` output | Effect on `count_tag(html, "b")` |
|---|---|---|---|---|
| `<B>` | `<` found; matching `>` found right after `B` | raw tag = `"B"`, lowercased = `"b"`, not a close tag (no leading `/`), name is not `br`/`p` -> strip | (nothing) | this IS an open `b` tag -> running count becomes `1` |
| `Hi` | plain characters, no `<` | copy through unchanged | `Hi` | unchanged |
| `<br>` | `<` found; matching `>` found right after `br` | lowercased name `"br"`, open tag -> special case | `\n` | unchanged |
| `bye` | plain characters | copy through unchanged | `bye` | unchanged |
| `</B>` | `<` found; matching `>` found; raw tag = `"/B"` | lowercased = `"/b"`, leading `/` means CLOSE tag -> strip, and close tags are never counted | (nothing) | unchanged (close tags do not count, even though the name matches) |
| `x` | plain character, no `<` | copy through unchanged | `x` | unchanged |
| `<bad` | `<` found; scan for `>` all the way to the end of the string and never find one | malformed (rule 2): treat this single `<` as a literal character and move on ONE character (not the whole `bad`) | `<` | unchanged (a malformed tag, having no `>`, is never counted, even though the letters `bad` are not the target name anyway) |
| `bad` | plain characters (now read one at a time, since the earlier `<` was consumed alone) | copy through unchanged | `bad` | unchanged |

Concatenating the "Appended" column in order gives the final result:

```
to_text("<B>Hi<br>bye</B>x<bad") == "Hi\nbyex<bad"
count_tag("<B>Hi<br>bye</B>x<bad", "b") == 1
```

Notice two easy-to-miss details this example is built to expose: (1) tag name
matching is case-insensitive, so the uppercase `<B>` still counts as a `b`
tag and still gets stripped by `to_text` the same way a lowercase `<b>`
would; and (2) a malformed tag consumes only the lone `<` character, not the
rest of the text after it -- so `<bad` at the end still contributes the
literal text `<bad` to the output, one character at a time, rather than
being swallowed whole.

---

## Learning goals

- Scan a string character by character, recognizing delimited tokens (`<...>`)
- Apply case-insensitive string comparison to tag names
- Distinguish open tags from close tags
- Organize a Catch2 test suite with named `TEST_CASE`s and tags
- Think adversarially (deliberately look for inputs that break your code,
  the way an attacker or a strict grader would): what inputs break a
  **naive implementation** (a straightforward first attempt that handles
  the common case but has not been checked against tricky inputs)?

---

## Task

Implement both functions declared in `html_parser.hpp` inside `html_parser.cpp`.

### `std::string to_text(const std::string& html)`

Strip all HTML tags and return the plain text.  Apply these rules in order:

1. Scan the input character by character.
2. When `<` is encountered, find the matching `>`.  If no `>` exists, treat the
   `<` as a literal character and continue.
3. The content between `<` and `>` is the raw tag string.  Extract the tag name
   by lowercasing the content and stripping any leading `/` for close tags.
4. Apply tag-specific transformations:
   - `<br>` (open tag only) -> append `\n` to the output
   - `<p>` (open tag only) -> append `\n\n` to the output
   - All other tags (including `<b>`, `<i>`, `<u>`, and unknown tags) -> strip
5. Characters outside any tag are appended to the output unchanged.

**Examples:**

- **Empty input:** `to_text("") == ""` -- **nothing to strip**.
- **Example (no tags):** `to_text("no tags here") == "no tags here"` -- no
  `<` at all, **every character is copied through unchanged**.
- **Example (basic strip):** `to_text("<b>Hi<br>there</b>") == "Hi\nthere"`
  -- `<b>` and `</b>` are stripped (they carry no special meaning), and
  **`<br>` becomes a newline**.
- **Tricky case (unmatched `<`):** `to_text("a < b") == "a < b"` -- the `<`
  here never finds a matching `>` anywhere in the rest of the string, so
  rule 2 says to treat it as a literal character; **the whole string passes
  through unchanged**.
- **Example (`<p>` tag):** `to_text("<p></p>") == "\n\n"` -- the open `<p>`
  appends `\n\n`; the close `</p>` is a close tag, so it is stripped and
  **contributes nothing**.
- **Example (case-insensitive):** `to_text("<BR>") == "\n"` -- tag names
  are matched case-insensitively (rule 3 lowercases before comparing), so
  **uppercase `<BR>` is still recognized as `br`**.

### `int count_tag(const std::string& html, const std::string& tag_name)`

Count the number of opening (non-closing) occurrences of `tag_name` in `html`.
Tag name matching is case-insensitive.  Malformed tags (no closing `>`) are not
counted.  Close tags (starting with `/`) are not counted.

**Examples:**

- **Empty input:** `count_tag("", "b") == 0` -- **nothing to count**.
- **Example (absent tag):** `count_tag("<b>hi</b>", "x") == 0` -- `tag_name`
  `"x"` **never appears at all**.
- **Example (case-insensitive, multiple):** `count_tag("<b><B><b>", "b") ==
  3` -- **three open tags**, matched case-insensitively (`<B>` counts the
  same as `<b>`).
- **Tricky case (close tag only):** `count_tag("</b>", "b") == 0` -- the
  only tag present is a CLOSE tag (starts with `/`), so it is not counted;
  **the open-tag count is zero**.
- **Tricky case (malformed tag):** `count_tag("<bad", "bad") == 0` -- `<bad`
  never finds a closing `>`, so it is malformed and is **not counted**, even
  though the tag name would otherwise match.

---

## Files

| File | Purpose |
|---|---|
| `html_parser.hpp` | Interface (the header file declaring the two functions' signatures, with no implementation) -- provided, do not modify |
| `html_parser.cpp` | Your implementation -- fill in the `TODO` sections |
| `CMakeLists.txt` | Build configuration -- wire Catch2 with FetchContent |
| `tests/test_html_parser.cpp` | Your test suite -- complete all required categories |

---

## Compilation and Testing

```bash
mkdir build && cd build
cmake ..
make
./html_parser_tests
```

Or to run with verbose output:

```bash
./html_parser_tests -v
```

---

## Constraints

- Do not use `<regex>` or any HTML-parsing library.
- Implement the parser using character-by-character scanning with `std::string`
  and the standard library only.
- `CMakeLists.txt` must use `FetchContent_Declare` and `FetchContent_MakeAvailable`
  to bring in Catch2 v3; no other method is accepted.
- Every `TEST_CASE` in `tests/test_html_parser.cpp` must include at least one
  `REQUIRE` or `CHECK` -- empty test cases do not count.

---

## Required test categories

Your test file must contain at least one non-empty `TEST_CASE` for every
category listed here.  The starter file already has the skeleton; fill them in.

| Category | Example input -> expected output |
|---|---|
| Empty input | `to_text("") == ""` |
| No tags | `to_text("hello") == "hello"` |
| Single tag pair | `to_text("<b>hi</b>") == "hi"` |
| Nested tags | `to_text("<b><i>hi</i></b>") == "hi"` |
| `<br>` tag | `to_text("a<br>b") == "a\nb"` |
| `<p>` tag | `to_text("x<p>y") == "x\n\ny"` |
| Case-insensitive tags | `to_text("<B>hi</B>") == "hi"` |
| Unknown tags stripped | `to_text("<span>hi</span>") == "hi"` |
| Text before first tag | `to_text("foo<b>bar</b>") == "foobar"` |
| Text after last tag | `to_text("<b>bar</b>baz") == "barbaz"` |
| Adjacent tags, no text | `to_text("<b></b>") == ""` |
| Multiple `<br>` tags | `to_text("a<br>b<br>c") == "a\nb\nc"` |
| Malformed tag (no `>`) | `to_text("hello <b world") keeps '<' as literal` |
| `count_tag` basic | `count_tag("<b>x</b>", "b") == 1` |
| `count_tag` ignores close tags | `count_tag("<b>x</b>", "b") == 1` (not 2) |
| `count_tag` case-insensitive | `count_tag("<B>x</B>", "b") == 1` |
| `count_tag` multiple | `count_tag("<b>x</b><b>y</b>", "b") == 2` |
| `count_tag` absent tag | `count_tag("<i>x</i>", "b") == 0` |

---

## Grading

| Component | Points |
|---|---|
| Correctness (hidden staff tests) | 60 |
| Test suite compiles and all cases pass against reference | 10 |
| Test suite detects seeded bugs in four buggy implementations | 30 |
| **Total** | **100** |
| Memory safety (Valgrind, extra credit) | +10 |

The fault-detection component runs your `tests/test_html_parser.cpp` against
four deliberately buggy implementations.  Each bug you catch earns 7.5 points.
Your tests must actually assert behavior -- a test that always passes cannot
catch any bugs.

---

## Submission

Submit `html_parser.cpp`, `CMakeLists.txt`, and `tests/test_html_parser.cpp`.
Do not modify `html_parser.hpp`.

---

## Going further

- Add a third function `bool is_balanced(const std::string& html)` that returns
  true when every `<b>`, `<i>`, and `<u>` open tag has a matching close tag.
- Handle attributes: `<b class="bold">` should strip to an empty string for the
  tag and pass through the text.
- Try running your test suite with `-fsanitize=address` (AddressSanitizer, or
  ASan -- a compiler flag that instruments your program to catch memory bugs
  like out-of-bounds reads while it runs) to catch any reads past the end of
  a string.
