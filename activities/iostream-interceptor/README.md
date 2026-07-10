# Activity: iostream Interceptor

A stream is an object that represents a flow of data in or out of a program,
one character at a time, hiding the details of where those characters
actually come from (the keyboard, a file, a string in memory). C++ streams
look simple on the surface -- you type `<<` and things appear on screen, you
type `>>` and values come in. But the stream model has a set of
precise rules about whitespace, state flags (internal bits such as `fail()`
and `good()` that record whether the last read or write succeeded), and what
happens when things go wrong. Getting these rules wrong is one of the most
common sources of silent bugs in beginner C++ programs.

This activity gives you seven short programs to predict. Each one isolates one
behavior of `std::istream` and `std::ostream`. You will be right about some and
surprised by others. The surprises are the point.

A note on output functions: C++23 introduced `std::print` and `std::println` as
convenient alternatives to `std::cout`. This course uses streams -- they are
more widely supported, more flexible, and they expose the underlying model that
makes all I/O in C++ work.

## Concepts covered

- `operator<<` chaining and left-to-right evaluation
- `operator>>` skips leading whitespace and stops at the next whitespace
- `std::getline` reads whitespace and does not skip leading spaces
- The leftover newline trap when mixing `>>` and `getline`
- Stream state flags: `fail()`, `good()`
- Why a failed stream ignores all subsequent reads
- `clear()` resets error flags without rewinding the stream position

## How it works

Seven C++ snippets are presented one at a time. Each uses `std::istringstream`
as a stand-in for `std::cin` -- the extraction and state behavior is identical,
but the input is fixed so you can reason about it precisely. For each snippet,
predict the exact output. Some snippets produce two lines; the launcher will
ask for each line separately.

After each answer, you will see whether you were right and a brief explanation
of why. Wrong answers do not advance the activity -- figure out the rule and
try again.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All seven snippets are answered correctly and the launcher prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- the >> / getline mixing problem</summary>

After `stream >> someInt`, the stream position sits immediately after the last
digit. If the input was `"42\nhello"`, the `'\n'` is still in the buffer.
The next `std::getline` call reads up to that `'\n'` and gets an empty string.

</details>

<details>
<summary>Hint 2 -- what happens after a failed extraction</summary>

When `>>` fails (for example, trying to read an `int` from `"abc"`), the
stream sets its `failbit`. Every subsequent `>>` on that stream is a no-op
until you call `stream.clear()`. The variable you tried to read is left
unchanged.

</details>

## Going further

- After calling `ss.clear()`, does the stream rewind to the beginning? Write
  a small program to verify, then check your mental model against the result.
- What does `std::ws` do? Try inserting `ss >> std::ws` between a `>>` and a
  `getline` and observe how it solves the leftover newline problem.
- Look up `std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n')`.
  When would you use this instead of `std::ws`?
- Try adding `std::boolalpha` to a stream before printing a `bool`. Does the
  manipulator persist across multiple `<<` calls?
