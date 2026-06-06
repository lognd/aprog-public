# Reverse String

Read a line from standard input and print it with the characters in reverse
order.

## Problem Statement

Your program reads a single line from stdin (not including the trailing
newline) and prints the reversed string followed by a newline.

## Input Format

- One line of text (printable ASCII, length >= 0)

## Output Format

- The same characters in reverse order, followed by a newline

## Examples

### Example 1

**Input:**
```
hello
```

**Output:**
```
olleh
```

### Example 2

**Input:**
```
racecar
```

**Output:**
```
racecar
```

### Example 3

**Input:**
```
abcde
```

**Output:**
```
edcba
```

## Constraints

- Input line length is at most 10,000 characters

## Grading

| Component   | Points |
|-------------|--------|
| Compilation | 0 (required) |
| Correctness | 100    |

## Submission

Submit a single file named `reverse-string.cpp`.
Compile command: `g++ -std=c++17 -Wall -o reverse-string reverse-string.cpp`
