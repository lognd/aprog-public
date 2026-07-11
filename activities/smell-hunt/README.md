# Activity: Smell Hunt

None of the code in this activity is broken. Every snippet compiles and
does exactly what it is supposed to do. That is the point: a CODE SMELL is
a pattern in working code that is not a bug, but signals that some future
change to that code is going to be harder or riskier than it should be.
Every snippet here comes with a short, plausible commit history in
comments, showing how the code got this way -- one reasonable decision at
a time, none of them wrong in isolation, adding up to something that rots.

## Concepts covered

- Recognizing five specific code smells by name:
  - shotgun surgery -- one conceptual change forces edits scattered
    across many separate places right now
  - copy-paste divergence -- two copies of the same logic have already
    silently drifted apart because a fix reached only one of them
  - rigid switch on type -- a function keeps growing one more
    if/else-if (or switch) branch every time a new case shows up
  - boolean parameter creep -- a function has accumulated so many
    true/false parameters that a call site like `doThing(true, false,
    true)` is unreadable without checking the signature
  - the god function -- one function has absorbed too many unrelated
    responsibilities (I/O, math, formatting, networking, ...) at once
- How each smell typically arises from a sequence of individually
  reasonable decisions, not one bad one
- Which refactor (restructuring code without changing what it does)
  direction fixes each smell: Strategy, Observer, or Extract Function
- The difference between shotgun surgery (one change, scattered edits,
  right now) and copy-paste divergence (two copies that have already
  drifted apart because a fix only reached one of them)

## How it works

You are shown nine small C++ snippets, each with a short comment history
explaining how it grew to its current shape. Each question gives you an
enumerated list of five possible code smells; type the name of the one
that snippet exhibits, exactly as written. A wrong answer gets a targeted
explanation of why that particular smell does not fit this snippet, and a
correct answer unlocks a fuller explanation naming which refactor
direction addresses the smell and why the rot happened in the first place
-- not because anyone wrote bad code on purpose, but because each addition
looked like the smallest reasonable change at the time.

## Getting started

```bash
python3 launch.py
```

No compiler is needed for this activity -- it is a plain
question-and-answer activity with C++ snippets shown as text, not compiled
or run.

## You will know you are done when...

You have correctly named the smell in all nine snippets and the activity
prints your passphrase.

## Hints

- Ask three questions about each snippet: What has to change if one new
  requirement shows up? Does that change land in one place or many? Is
  everything in this function actually about the same job?
- Shotgun surgery and copy-paste divergence are easy to mix up. Shotgun
  surgery is about the PAIN of one change needing to reach several
  scattered places right now. Copy-paste divergence is about two copies
  that have ALREADY silently drifted apart because a fix reached only one
  of them.
- Boolean parameter creep often hides in a function's call site, not its
  body -- if you cannot tell what `doThing(true, false, true)` means
  without checking the function signature, that is the smell.
