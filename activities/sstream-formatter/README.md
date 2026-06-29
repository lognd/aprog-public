# Activity: String Stream Formatter

Output formatting in C++ is controlled by stream manipulators -- objects you
insert into a stream to change how subsequent values are printed. They control
field width, fill character, alignment, floating-point notation, integer base,
and more. Most manipulators are "sticky": once set, they persist until you
change them. One important manipulator, `std::setw`, is the famous exception.

`std::ostringstream` lets you build a formatted string entirely in memory using
the same operator<< syntax as `std::cout`. When the string is ready, you call
`.str()` to extract it. This makes `ostringstream` ideal for building formatted
output before deciding where to send it.

This activity presents seven short programs using `<iomanip>` manipulators.
Predict the exact output of each one -- spaces, zeros, stars, and all.

## Concepts covered

- `std::ostringstream` as an in-memory output buffer; `str()` to extract the string
- `std::setw` is one-shot: it resets to 0 after each insertion
- `std::setfill`, `std::left`, `std::right`, `std::fixed`, `std::hex`, `std::showbase`, and `std::boolalpha` are sticky
- `std::setprecision` controls decimal digits for floating-point output
- `std::hex` + `std::showbase` and the special case of zero

## How it works

Seven C++ snippets are presented one at a time. Each one applies a combination
of manipulators and prints the result. Predict the exact output -- character for
character, including spaces and fill characters. Some snippets produce multiple
lines; the launcher will ask for each line separately.

After each answer you will see the explanation of why that output is correct.
Wrong answers do not advance the activity.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All seven snippets are answered correctly and the launcher prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- which manipulators are sticky vs. one-shot</summary>

Almost every manipulator is sticky -- it stays in effect until you change it.
The one famous exception is `std::setw`: it applies to exactly the next item
inserted, then resets to 0.

</details>

<details>
<summary>Hint 2 -- setw and setfill together</summary>

`std::setfill` is sticky, but `std::setw` is not. If you call
`std::setfill('0') << std::setw(4)` and then insert a value, the '0' fill
persists for the next `setw` call, but you have to call `setw` again to get
any padding.

</details>

<details>
<summary>Hint 3 -- zero is a special case for showbase</summary>

`std::showbase` adds the `0x` prefix for non-zero hexadecimal values.
The value 0 is printed without a prefix regardless of `showbase`.

</details>

## Going further

- What does `std::noshowbase` do? Try toggling it mid-output to confirm your
  mental model of stickiness.
- `std::setprecision` without `std::fixed` uses "default" floating-point
  notation, where precision means significant digits, not decimal places. Try
  removing `std::fixed` from snippet 5 and predict the new output.
- `std::uppercase` makes the `0x` prefix and hex digits uppercase (`0XFF`
  instead of `0xff`). Predict what snippet 6 would print with `std::uppercase`
  added.
- Build a small table-printer using `std::ostringstream` that formats three
  columns of data with fixed widths. Use `std::left` for the name column and
  `std::right` for the numeric columns.
