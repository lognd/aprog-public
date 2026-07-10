# Activity: CLI Contract Discovery

A compiled binary called `./cowfarm` is waiting in your shell with no source
code attached. Your job is to figure out its complete interface by running it
with different arguments, reading its output carefully, and writing down what
you learn. This is exactly what you do every time you encounter an unfamiliar
command-line tool in the wild.

The catch: the characters have formal given names, not species labels. You
cannot guess them -- you have to find them.

## Concepts covered

- `argc` and `argv` as the mechanism behind CLI flags and positional arguments
- Distinguishing flags (`--flag`, an optional named switch usually starting
  with `-` or `--`) from positional arguments (`CHARACTER MESSAGE`, values
  identified by their order rather than a name)
- The `-h`/`--help` and `--list` conventions as a tool's self-documentation
- `usage:` as the standard no-argument error convention -- a one-line summary
  of how to invoke the program, printed when it is run incorrectly or asked
  for help
- Reading a binary's behavior as a black box (a program you can only run and
  observe, with no source code to read) before writing any code

## How it works

The launcher opens a shell containing a single compiled binary, `./cowfarm`.
No source code is visible. You explore it freely, then `exit` the shell. The
launcher then asks four questions about what you found. All four correct answers
unlock the passphrase.

The questions ask for exact names and flags -- not descriptions, not species.
Read the output of the tool carefully.

## Getting started

```bash
python3 launch.py
```

A shell opens with `./cowfarm` ready to run.

### Step 1 -- read the usage message

Run `./cowfarm` with no arguments and read the output carefully.

### Step 2 -- explore the flags

Try `-h`, `--help`, and `--list`. Note what each one prints.

### Step 3 -- meet every character

Run `./cowfarm` with each character name and a short message. Read the
`--list` output and write down each character's exact name.

### Step 4 -- exit

```bash
exit
```

The launcher asks four questions. Answer based on what you observed.

## You will know you are done when...

The launcher prints `Passphrase:` followed by the unlock phrase. All four
questions must be answered correctly with the exact strings the tool itself
showed you.

## Hints

<details>
<summary>Hint 1 -- you missed a flag</summary>

There are three flags total. Run `./cowfarm --help` and read every line of
the output -- it lists all of them explicitly.

</details>

<details>
<summary>Hint 2 -- the character names are not what you expect</summary>

The character names are formal given names, not the names of the species
they depict. Run `./cowfarm --list` and copy the names exactly as printed.

</details>

<details>
<summary>Hint 3 -- the no-argument question</summary>

Run `./cowfarm` with nothing and look at the very first word on the first
line of output. Include any punctuation attached to it.

</details>

## Going further

- Try passing an unknown flag like `./cowfarm --verbose hello world`. What
  does the error message tell you? Compare this to what `--help` prints.
- Write your own version of `cowfarm` usage output from memory. Then run
  `./cowfarm --help` and compare. What did you miss or get wrong?
- Pick any CLI tool you use regularly (`ls`, `git`, `g++`) and write its
  usage string from memory before checking with `--help`. How close were you?
- Look up the POSIX (Portable Operating System Interface, the standard that
  defines common conventions across Unix-like systems) utility argument
  syntax conventions and compare them to what `cowfarm` does. Which
  conventions does it follow? Which does it skip?
