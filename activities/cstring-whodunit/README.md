# Activity: C-String Whodunit

Recognizing classic C-style string bugs: buffer overflows, pointer
comparisons used instead of `strcmp`, writing to string literals,
`sizeof` vs `strlen` confusion, and `strncpy`'s silent null-terminator
omission.

## Concepts covered

- Buffer overflow: writing past the end of a fixed-size `char` array
- Pointer comparison vs `strcmp`: `==` on two `char*` compares addresses, not content
- Writing to string literals: undefined behavior (the C++ standard places
  no limit on what happens -- crash, corruption, or silent "success") because
  literals are read-only
- `sizeof` vs `strlen`: `sizeof` gives the array size, `strlen` gives the string length
- `strncpy` and the silent null-terminator omission when the source fills the buffer

## How it works

Seven buggy or tricky code situations are described one at a time. For
each one, diagnose what is wrong (or what happens) and type your answer.
Correct diagnoses unlock an explanation of the real failure mode.

No compilation needed -- read, reason, and answer.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All seven diagnoses are correct and the program prints the passphrase.

## Going further

- Write a buffer overflow deliberately in a `char[8]` and run it under
  ASan. Find where in the report it tells you the allocation size and the
  offset of the first out-of-bounds write.
- Look up `strncpy` in the C standard. Find the exact wording that explains
  why it does not null-terminate when `src` fills the buffer -- and note
  the alternative (`strlcpy`) that fixes this.
- Find a real CVE (Common Vulnerabilities and Exposures) that is attributed
  to a `strcmp`-vs-pointer-comparison bug in C code.
