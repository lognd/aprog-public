# Activity: argv Explorer

How C++ programs receive arguments from the command line: the `argc` count,
the `argv` array of C strings, the guaranteed null sentinel at `argv[argc]`,
and how to convert string arguments to integers.

## Concepts covered

- The `argc` count and `argv` array layout in memory
- The null sentinel at `argv[argc]` guaranteed by the C standard
- Converting string arguments to integers with `atoi` / `strtol`
- Input validation patterns for command-line programs

## How it works

Seven questions covering `argc`, `argv` layout, argument conversion, and
input validation. The activity unlocks when all answers are correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All seven questions are correct and the program prints the passphrase.

## Going further

- What happens if you access `argv[argc]`? The standard guarantees it is
  `nullptr` -- write a small program to verify that and look at the assembly.
- Write a simple option parser that handles `--key=value` style arguments
  without using any standard library parsing utilities.
- What does `strtol` return when the input is not a valid number? Read the
  man page and write a version of the converter that detects and reports errors.
