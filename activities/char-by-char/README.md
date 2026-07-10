# Activity: Char by Char

The fundamental loop pattern for walking C-style strings character by
character. A C-style string is just an array of `char` with no stored
length -- code finds the end by scanning for a sentinel (a special marker
value meaning "stop here"), the byte `'\0'`. Every C string function you
will ever write -- `strlen`, `strcpy`, `reverse`, `contains` -- reduces to
this one loop. You will also see how pointer arithmetic and the two-pointer
technique (walking two positions through the same array at once, e.g. one
from each end) emerge naturally from this pattern.

## Concepts covered

- The null-terminated C string sentinel pattern (`'\0'` marking where the
  real data ends and the loop should stop)
- Pointer increment (`p++`) as character-by-character string traversal
- How `strlen`, `strcpy`, and `reverse` all reduce to the same loop skeleton
- The two-pointer technique for in-place string operations

## How it works

Six short C++ programs are shown one at a time. Predict what each one
prints, then press Enter to check. Correct answers unlock an explanation.
All six correct answers together unlock the passphrase.

You do not need to compile anything -- read the code and think it through.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six answers are correct and the program prints the passphrase.

## Going further

- Implement `strlen`, `strcpy`, and `strcat` from scratch using only pointer
  arithmetic -- no index variables, no `[]`.
- Compile a simple pointer loop and an equivalent index loop with `g++ -S -O2`
  and compare the assembly output. Are they identical?
- What happens if you pass a `char*` that is not null-terminated to `strlen`?
  Demonstrate the undefined behavior (a category of bug where the C++
  standard places no limit on what happens -- crash, garbage output, or
  something that looks fine until it isn't) with AddressSanitizer
  (`-fsanitize=address`, a compiler tool that detects memory errors like
  out-of-bounds reads at runtime).
