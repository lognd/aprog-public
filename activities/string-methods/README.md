# String Methods -- Fix the Word Wrapper

Word-wrapping means breaking a long string of text into lines that each fit
within a maximum column width, always cutting at a space between words rather
than in the middle of one.

The C++ function in this activity is supposed to do that, but it has two
bugs.  One causes lines to break one word too early.  The other silently
drops the last line entirely.

When both bugs are fixed the output has exactly five lines.  Read the first
letter of each line in order -- those five letters spell the LMS passcode for
this activity.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the project.

## Walk-through

### Step 1 -- compile and run the broken program

    make run

The program prints however many lines the broken function produces, along
with a count.  It also tells you whether that count is correct.  Read the
output carefully and note what looks wrong.

### Step 2 -- open wrap.cpp and read the function

The function `word_wrap` works by going through the words one at a time and
building up a `current` line.  When adding the next word would make `current`
too long, it saves `current` to the `lines` vector and starts a new one.

Find the two bugs:

- **Bug 1** is a one-character mistake in the `else if` condition that checks
  whether a word fits on the current line.
- **Bug 2** is a missing statement after the loop ends.  Think about what
  happens to the last value of `current` when the loop finishes.

### Step 3 -- fix both bugs and rerun

    make run

The program will tell you if the output has the right number of lines.  Both
bugs must be fixed at the same time -- fixing only one will not produce
correct output.

### Step 4 -- read the first letter of each line

Look at the five lines of output.  Write down the first letter of each, in
order, as a single word.

### Step 5 -- exit

    exit

Write down the first letter of each of the 5 output lines in order before
you exit.  That word is the LMS passcode -- submit it directly.

## You'll know you're done when...

The program prints exactly 5 lines and says "Correct!"

## Hints

<details>
<summary>Hint 1 -- Bug 1: the comparison operator</summary>

The `else if` condition decides whether `word` fits on `current` without
exceeding `width`.  It currently uses `<` (strictly less than).  That means
a line that would be exactly `width` characters long gets rejected and broken
one word too early.  Change `<` to `<=`.

</details>

<details>
<summary>Hint 2 -- Bug 2: the missing statement</summary>

After the `for` loop, `current` holds the last line that was being built.
The function returns without ever saving it.  Add this before `return lines;`:

    if (!current.empty())
        lines.push_back(current);

</details>

<details>
<summary>Hint 3 -- checking your work</summary>

After fixing both bugs, each line should be at most 36 characters long and
there should be exactly 5 of them.  If you still see the wrong count, make
sure you fixed both bugs -- they interact, so one fix alone will not be
enough.

</details>
