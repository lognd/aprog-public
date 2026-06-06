# Word Count

Count the words on each line of stdin and print per-line and total word counts.

## Problem Statement

Read lines from standard input until EOF. For each line, print how many
whitespace-delimited words it contains. After all lines, print the total.

## Output Format

For each line `i` (1-indexed):
```
Line i: W words
```
After all lines:
```
Total: W words
```

Use `word` (singular) when the count is 1, `words` (plural) otherwise.

## Examples

### Example 1

**Input:**
```
hello world
foo bar baz
one
```

**Output:**
```
Line 1: 2 words
Line 2: 3 words
Line 3: 1 word
Total: 6 words
```

### Example 2

**Input:**
```
the quick brown fox
```

**Output:**
```
Line 1: 4 words
Total: 4 words
```

## Grading

| Component   | Points |
|-------------|--------|
| Build       | 10     |
| Correctness | 90     |

## Submission

Submit `Makefile` and all required source files. `make` must produce a
binary named `word-count`.
