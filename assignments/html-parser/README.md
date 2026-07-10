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

### `int count_tag(const std::string& html, const std::string& tag_name)`

Count the number of opening (non-closing) occurrences of `tag_name` in `html`.
Tag name matching is case-insensitive.  Malformed tags (no closing `>`) are not
counted.  Close tags (starting with `/`) are not counted.

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
