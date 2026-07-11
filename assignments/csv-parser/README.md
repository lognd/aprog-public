# CSV Parser

Implement a single C++ function that parses CSV text into a
`std::vector<std::vector<std::string>>`.

---

## Learning goals

- Parse a structured text format by iterating characters and tracking parser state (remembering things like "am I currently inside a quoted field?" as you move character by character)
- Handle quoting and escaping without regular expressions or external libraries
- Build nested `std::vector<std::vector<std::string>>` from a streaming input (text handled a chunk at a time rather than all parsed at once)
- Write a function that correctly handles edge cases (empty fields, trailing commas, short rows)

## Background

CSV (Comma-Separated Values) is deceptively simple to parse.  The naive
approach -- splitting on commas -- breaks as soon as a field contains a comma
inside quotation marks.  A correct parser must handle quoting, escaping, and
several structural edge cases.

This lab is purely a strings-and-vectors exercise.  No classes, no file I/O,
no external libraries -- just iterating characters, building strings, and
storing them in a `vector<vector<string>>`.

---

## What to implement

Fill in the body of `parse_csv` in `csv_parser.hpp`.  Do not change the
signature.

```cpp
std::vector<std::vector<std::string>> parse_csv(std::string text);
```

Each element of the outer vector is one row.  Each element of the inner
vector is one field.  Row 0 is the first line of the input.

*Examples (all confirmed against the reference solution):*
- `parse_csv("a,b,c")` -> `{{"a", "b", "c"}}` -- one row, three plain fields.
- `parse_csv("a,\"b,c\"")` -> `{{"a", "b,c"}}` -- the comma inside quotes does
  not split the field; see the step-by-step trace below for exactly why.
- `parse_csv("a,\"say \"\"hi\"\"\",b")` -> `{{"a", "say \"hi\"", "b"}}` -- the
  `""` escape inside a quoted field collapses to one literal `"`.
- `parse_csv("")` -> `{{}}` -- one row with **zero fields**, not zero rows;
  `parse_csv` never returns an empty outer vector.
- `parse_csv("a,b\n\nc,d")` -> `{{"a","b"}, {}, {"c","d"}}` -- the blank line
  in the middle produces its own zero-field row rather than being skipped.
- There is no error case: `parse_csv` takes a `std::string` and always
  returns some `vector<vector<string>>`, even for malformed-looking input
  like an unterminated quote -- there is nothing for it to throw or fail on.

### Parsing rules (RFC 4180 subset)

RFC 4180 is the internet standard document that defines the CSV format
precisely (how quoting, escaping, and line endings work). You are
implementing a subset of it -- just the rules in the table below.

| Situation | Rule |
|-----------|------|
| Plain field | Characters up to the next `,` or end-of-line |
| Quoted field | Starts with `"`, ends with `"`, may contain commas and newlines |
| Escaped quote | `""` inside a quoted field means a single literal `"` |
| Empty field | `a,,b` produces `{"a", "", "b"}` |
| Trailing comma | `a,b,` produces `{"a", "b", ""}` |
| Empty line | Produces a row with zero fields -- do not skip it |
| Short row | A row with fewer fields than other rows is **not** an error -- return however many fields that line actually contains; do not pad with empty strings |
| Line endings | Support both `\n` and `\r\n` |
| Whitespace | Not trimmed -- spaces are part of the field value |

---

## Files

| File | Your role |
|------|-----------|
| `csv_parser.hpp` | Implement `parse_csv` |
| `visible-tests/test_csv_parser.cpp` | Run locally to check your work |

Do **not** modify `visible-tests/test_csv_parser.cpp`.

---

## Example

Input:
```
Name,City,Score
Alice,"Portland, OR",92
Bob,"Said ""hi""",88
Carol,,75
```

Expected output of `parse_csv(text)`:
```
rows[0] = {"Name",  "City",         "Score"}
rows[1] = {"Alice", "Portland, OR", "92"   }
rows[2] = {"Bob",   "Said \"hi\"",  "88"   }
rows[3] = {"Carol", "",             "75"   }
```

Each row is independent -- `rows[i].size()` may differ from `rows[j].size()`.
The parser does not pad short rows or truncate long ones.

---

## Examples at a glance

To make the tricky cases concrete, here is **one** representative line, with
exactly what `parse_csv` produces for it. This line packs in an embedded
comma inside quotes, an empty field, and an escaped quote, all at once:

```
101,"Smith, John",,"He said ""hi"""
```

| Field index | Value produced | Why |
|---|---|---|
| 0 | `"101"` | plain field, read up to the next comma |
| 1 | `"Smith, John"` | the field starts with `"`, so the comma inside it is just part of the field's text, not a separator -- the field ends only at the matching closing `"` |
| 2 | `""` | two commas in a row with nothing between them means an empty field, not a skipped one |
| 3 | `He said "hi"` (shown with real quote characters) | `""` inside a quoted field is RFC 4180's escape for a single literal `"` -- so `""hi""` becomes `"hi"` in the final string |

`parse_csv` returns one row containing exactly these 4 fields:
`rows[0] = {"101", "Smith, John", "", "He said \"hi\""}`.

Two more small cases worth knowing, each confirmed by running the reference
solution:

| Input | Output | Why |
|---|---|---|
| `""` (empty string, zero characters) | `rows.size() == 1`, `rows[0].size() == 0` | an empty input is still one (empty) row, not zero rows |
| `"a , b ,c"` | `rows[0] = {"a ", " b ", "c"}` | whitespace around commas is not trimmed -- the spaces are kept exactly as typed |

---

## Worked example: parsing one line, step by step

This traces `parse_csv("a,\"b,c\"")` -- the C++ string literal
`a,"b,c"` -- one character at a time, ending at the exact fields the
function returns: `{"a", "b,c"}`.

| Step | Character read | Parser state | Field buffer so far | Action / reason |
|------|-----------------|---------------|----------------------|------------------|
| 1 | `a` | outside quotes | `a` | not a comma, quote, or line ending -- append it to the current field |
| 2 | `,` | outside quotes | `a` (field closes) | a bare comma outside quotes ends the current field; push `"a"` into the row, start a new field |
| 3 | `"` | field starts quoted | (empty) | a field that starts with `"` is a quoted field -- enter "inside quotes" mode; the quote character itself is NOT added to the field |
| 4 | `b` | inside quotes | `b` | inside quotes, ordinary characters are appended just like normal |
| 5 | `,` | inside quotes | `b,` | **this comma is inside quotes**, so it is just a character to append, not a field separator -- this is the whole point of quoting |
| 6 | `c` | inside quotes | `b,c` | still inside quotes, appended normally |
| 7 | `"` | closing quote found | `b,c` (field closes) | this `"` is not followed by another `"`, so it is a plain closing quote (not an escaped `""`) -- exit quoted mode and push `"b,c"` into the row |
| end | (end of input) | -- | -- | no more characters; the row `{"a", "b,c"}` is complete and becomes `rows[0]` |

The key moment is step 5: an ordinary (unquoted) parser would have split the
field there and produced three fields instead of two. Tracking "am I
currently inside a quoted field?" as a piece of state, and consulting it
before treating a comma as a separator, is the one idea that makes the rest
of this assignment work.

---

## Building and testing

```bash
g++ -std=c++17 -o test visible-tests/test_csv_parser.cpp
./test
```

## Grading

| Component                | Points |
|---------------------------|--------|
| Compilation                | 0*     |
| simple_row                 | 8      |
| two_rows                   | 7      |
| crlf                       | 7      |
| quoted_comma                | 8      |
| escaped_quote               | 8      |
| quoted_newline              | 8      |
| empty_middle                | 7      |
| trailing_comma              | 7      |
| empty_line                  | 7      |
| readme_example              | 8      |
| multiline_quoted_rows       | 7      |
| all_empty_fields            | 5      |
| whitespace_not_trimmed      | 5      |
| single_column               | 5      |
| many_rows                   | 3      |
| **Total**                  | **100** |

`*` Compilation is a gate, not a scored component -- your submission must
compile before any test case can run.

## Submission

Submit a single file named `csv_parser.hpp`. Do not rename it.

## Going further

- Extend `parse_csv` to support `\r\n` line endings if it does not already,
  and write a test case with Windows-style line endings.
- Implement a `serialize_csv` function that goes the other direction: takes
  a `vector<vector<string>>` and produces valid RFC 4180 CSV text.
- Look up what happens when a quoted field contains a newline. Does your
  parser handle multi-line fields?
