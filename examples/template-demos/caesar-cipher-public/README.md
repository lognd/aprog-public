# Caesar Cipher

Encrypt a message using a Caesar cipher: shift each letter by a given number
of positions in the alphabet.

## Problem Statement

Your program receives the shift amount as a command-line argument (`argv[1]`).
It then reads text from stdin and writes the encrypted text to stdout.
Only letters (`a-z`, `A-Z`) are shifted; all other characters are passed
through unchanged. Case is preserved. The shift wraps around (mod 26).

## Usage

```
./caesar-cipher <shift>
```

The shift can be any integer (positive, negative, or zero).

## Examples

### Example 1 -- shift by 3

**Command:** `echo "Hello, World!" | ./caesar-cipher 3`

**Output:**
```
Khoor, Zruog!
```

### Example 2 -- shift by 13 (ROT13)

**Command:** `echo "Hello" | ./caesar-cipher 13`

**Output:**
```
Uryyb
```

### Example 3 -- shift by 0

**Command:** `echo "abc" | ./caesar-cipher 0`

**Output:**
```
abc
```

## Constraints

- Shift is passed as `argv[1]`; you may assume it is a valid integer
- Input may contain multiple lines; process all of them
- Non-letter characters pass through unchanged

## Grading

| Component   | Points |
|-------------|--------|
| Compilation | 0 (required) |
| Correctness | 100    |

## Submission

Submit a single file named `caesar-cipher.c`.
