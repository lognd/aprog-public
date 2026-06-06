# CSV Parser

Implement a single C++ function that parses CSV text into a
`std::vector<std::vector<std::string>>`.

---

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
std::vector<std::vector<std::string>> parse_csv(const std::string& text);
```

Each element of the outer vector is one row.  Each element of the inner
vector is one field.  Row 0 is the first line of the input.

### Parsing rules (RFC 4180 subset)

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

## Building and testing

```bash
g++ -std=c++17 -o test visible-tests/test_csv_parser.cpp
./test
```
