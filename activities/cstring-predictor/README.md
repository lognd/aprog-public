# Activity: C-String Predictor

Before `std::string` existed, C++ inherited C's model of strings: a plain
array of `char` ending in a special sentinel byte, `'\0'`. No length field,
no bounds checking, no automatic memory management -- everything is derived
by scanning for that one byte. This activity trains you to trace a C-style
string byte by byte so that functions like `strlen`, `strcpy`, and `strcat`
stop feeling like magic and start feeling like simple loops.

## Background

A C string is just a `char` array with a convention layered on top: the
first `'\0'` byte marks the end. Declaring `char s[] = "hello";` allocates 6
bytes, not 5 -- the compiler appends the terminator for you:

```
s:  [0]='h' [1]='e' [2]='l' [3]='l' [4]='o' [5]='\0'
sizeof(s) == 6      strlen(s) == 5
```

`sizeof` and `strlen` answer different questions, and confusing them is one
of the most common C-string bugs. `sizeof(s)` is a compile-time property of
the array's declared size -- it counts every byte, including the
terminator. `strlen(s)` is a runtime scan that walks forward from `s[0]`
counting bytes until it finds `'\0'`, and that count does not include the
terminator itself. If you shrink the "string" by writing an early `'\0'`
partway through the array, `strlen` stops there even though the array's
declared size, and `sizeof`, do not change:

```cpp
char buf[5] = {'h', 'i', '\0', 'x', 'y'};
// buf:  [0]='h' [1]='i' [2]='\0' [3]='x' [4]='y'
std::cout << buf << "\n";        // prints "hi"   -- stream stops at '\0'
std::cout << strlen(buf) << "\n"; // prints 2      -- scan stops at '\0'
```

Everything downstream of "print a C string" or "measure a C string" only
ever looks as far as the first `'\0'`. The bytes after it -- `'x'` and `'y'`
above -- still physically exist in the array, but no string function will
ever see them.

**The core `<cstring>` functions, traced as loops:**

- `strlen(s)`: start a counter at 0, walk forward while `s[i] != '\0'`,
  incrementing the counter each step. Return the counter -- never the
  terminator itself.
- `strcpy(dst, src)`: walk `src` from the start, copying each byte into the
  matching position in `dst`, including the final `'\0'`. Nothing checks
  that `dst` is large enough to hold `src` -- that is entirely your
  responsibility as the caller.
- `strcat(dst, src)`: first walk `dst` forward to find its own terminator
  (exactly like `strlen` would), then starting at that position, copy
  `src` byte by byte the same way `strcpy` does, ending with a fresh
  `'\0'`. `strcat` never touches `dst`'s existing characters -- it only
  finds where they end.

A buffer's declared *size* (how many bytes it can hold) and a string's
*length* (how many bytes are meaningful right now) are independent numbers.
`char buf[20];` can hold a string of up to 19 real characters plus the
terminator, but at any moment it might hold a much shorter string, or none
at all if uninitialized. Building a string with `strcpy` then `strcat`
grows the length while the size stays fixed:

```cpp
char buf[20];
strcpy(buf, "foo");   // buf now holds "foo\0", length 3, capacity 20
strcat(buf, "bar");   // buf now holds "foobar\0", length 6, capacity 20
```

Finally, remember that a `char[]` decays to a `const char*` the moment you
pass it to a function or assign it to a pointer variable -- the array and a
pointer to a string literal look the same once you only have the pointer,
but only the array's own storage is writable. `const char* s = "dog";`
points at read-only memory; `s[0] = 'x';` would be undefined behavior, while
`char s[] = "dog"; s[0] = 'x';` is perfectly fine because the array is your
own local storage.

## Concepts covered

- Null-terminated character arrays and the `'\0'` sentinel
- `sizeof` (declared byte count) vs `strlen` (scan-based length up to `'\0'`)
- `strlen`, `strcpy`, `strcat`: what each one actually does, traced as a loop
- Buffer capacity vs. string length as independent, changing quantities
- Pointer decay: how a `char[]` becomes a `const char*`, and why only the
  array's own storage is writable

## How it works

You are shown six short C++ programs that declare char arrays or pointers
and call `<cstring>` functions on them. For each one, predict the exact
output before running it -- some print one line, some print two. The
launcher compiles and actually runs each snippet, then checks your answer
against the real output character-for-character. The activity unlocks when
all six predictions are correct.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All six predictions are correct and the program prints the passphrase.

## Hints

<details>
<summary>Hint 1 -- tracing a snippet by drawing the array</summary>

For any snippet with a `char` array, draw a row of boxes, one per element,
and fill in the initial values, including the `'\0'` if one is given
explicitly. Then step through the code line by line, updating only the
boxes that change. Whenever the code prints the array (`std::cout << buf`),
read left to right from index 0 and stop at the first `'\0'` -- that is
exactly what the stream does.

</details>

<details>
<summary>Hint 2 -- sizeof is not strlen</summary>

`sizeof` on an array is a compile-time constant equal to however many bytes
were declared or inferred from the initializer -- it never changes at
runtime and always includes the terminator slot. `strlen` is a runtime scan
that can return a smaller number if a `'\0'` appears before the end of the
array.

</details>

<details>
<summary>Hint 3 -- strcat needs to find the end of dst first</summary>

Before appending anything, `strcat` behaves like `strlen(dst)` internally --
it scans forward from `dst[0]` until it finds the existing terminator, and
that is where the new characters start getting written. If you forget this
step when tracing by hand, you will place the appended text in the wrong
position.

</details>

## Going further

- Implement `strcat` from scratch: walk to the end of `dst`, then copy `src`
  character by character. How does the final null terminator get placed?
- What does `strlen` return for an empty string (`""`)? Verify your answer
  by tracing the loop.
- Write a program that deliberately overflows a `char[8]` buffer and run it
  under ASan (`-fsanitize=address`) to see what the report looks like.
- Change one of the six snippets to use `std::string` instead of a raw
  `char` array. What operations get simpler, and what do you lose control
  over?
