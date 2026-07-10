# Study Guide 3: What Is a Computer?

This is the foundations lecture: before any C++ syntax, students need a
mental model of what a computer physically is and does -- memory as a long
row of numbered bytes, binary and hexadecimal as ways of writing byte
values, the CPU as a tiny set of fast registers cycling through
fetch-decode-execute, and the idea that a C++ program is just a
translation, several layers deep, down to numbers a CPU can run. No
artifact accompanies this row; it is taught in lecture, and every later
row of this course silently assumes the student has this mental model.

## Know before you start

- Nothing beyond row 2's environment setup (a working shell and the
  ability to run a program).

## Taught here

Concept: memory as a numbered row of bytes
- Know that computer memory (RAM) is a long, flat row of storage slots
  called bytes, each one holding a single number from 0 to 255 (a byte is
  8 bits, and 2^8 = 256 possible values, numbered 0 through 255).
- Know that every byte has an address: its position (index) in that row,
  counting from 0. An address is just a number, exactly like a house
  number on a street.
- Analogy: think of memory as a single, extremely long street of
  mailboxes, each with a house number painted on it (the address) and
  each capable of holding one small note with a number from 0 to 255
  written on it (the byte's value). "Read byte 1024" means "walk to
  mailbox 1024 and read what is inside."
- Know the single most important idea in this course: everything a
  computer works with -- numbers, text, images, running programs
  themselves -- is ultimately just bytes sitting in this row. Nothing is
  stored as "text" or "a number" in any special way memory can see; it is
  bytes, and it is only ever the reading program that decides how to
  interpret them.
- Concrete example, text as bytes: the two-character text "Hi" is stored
  as exactly two bytes: 72 (the character 'H') and 105 (the character
  'i'), back to back at two consecutive addresses. There is no separate
  "this is text" marker attached to those bytes; a program only treats
  them as text because it chose to (for example, by printing them using a
  rule that maps 72 to the letter 'H').
- Concrete example, a number needing more than one byte: a single byte
  can only hold 0 to 255, so the number 300 cannot fit in one byte. A
  program storing 300 uses two consecutive bytes together and combines
  them (for example, storing 300 as the two bytes 44 and 1, then
  computing 44 + 1*256 = 300 to read it back) -- this is exactly why C++
  has types like `int` that reserve a fixed number of bytes (commonly 4)
  for a value, instead of one.

Concept: binary and hexadecimal
- Know that a computer's underlying hardware stores and moves information
  as binary (base 2: only the digits 0 and 1), because the simplest,
  cheapest, most reliable physical way to represent a value in a wire or
  a transistor is two states: a wire either has voltage on it (1) or does
  not (0). Building hardware that reliably distinguished ten different
  voltage levels (for base 10) would be far more error-prone and
  expensive than reliably distinguishing two.
- Know that a bit is a single binary digit (0 or 1), and a byte is 8 bits
  strung together, read as an 8-digit binary number.
- Concrete conversion: the byte value 72 (decimal, base 10) is 01001000
  in binary -- read right to left, that is 0*1 + 0*2 + 0*4 + 1*8 + 0*16 +
  0*32 + 1*64 + 0*128 = 8 + 64 = 72.
- Know that hexadecimal (base 16, digits 0-9 then A-F for 10-15) exists
  purely as a compact, human-friendly notation for binary: each hex digit
  represents exactly 4 bits, so a full byte (8 bits) is always exactly 2
  hex digits, and hex-to-binary conversion is a simple digit-by-digit
  lookup with no arithmetic needed (unlike converting to or from decimal).
- Know the `0x` prefix is C++'s (and most languages') way of writing a
  hexadecimal literal in source code, e.g. `0x48`.
- Concrete conversion: the byte value 72 (decimal) is 0x48 in hex (4*16 +
  8 = 64 + 8 = 72), and 0x48 in binary is 0100 1000 -- the same 8 bits as
  above, just grouped into two 4-bit nibbles (0100 = 4, 1000 = 8) instead
  of read as one 8-digit number.

Concept: the CPU -- registers, the fetch-decode-execute cycle, the clock
- Know that the CPU (Central Processing Unit) cannot operate directly on
  values sitting out in main memory; it has a small, fixed number of
  named registers -- tiny storage slots built directly into the CPU chip
  itself, holding one value each (commonly one machine word, e.g. 8 bytes
  on a 64-bit CPU).
- Know that registers are dramatically faster to access than main memory
  (often 100x or more), simply because they are physically inside the
  CPU with essentially no distance for an electrical signal to travel,
  while memory sits on separate chips reached over a bus (a set of wires
  connecting components).
- Know the load-operate-store pattern this implies: to add two numbers
  that live in memory, the CPU must first load each one from memory into
  a register, perform the addition using only register values, and then
  store the result back out to memory if it needs to persist. A CPU
  instruction like "add" only ever operates on registers (or a register
  and a small embedded constant), never directly on two memory addresses
  at once.
- Analogy: registers are like the handful of items you are currently
  holding in your two hands while cooking -- blazing fast to use, but
  there are only so many hands. Main memory is the pantry down the hall:
  it holds everything else, but every trip there and back costs real
  time. You do not cook directly out of the pantry; you fetch what you
  need into your hands first.
- Know the fetch-decode-execute cycle, the loop every CPU runs
  continuously, billions of times per second: fetch (read the next
  instruction's bytes from memory), decode (figure out which operation
  those bytes mean and which registers/values it needs), execute (
  actually perform that operation), then repeat for the next instruction.
- Know the clock is a hardware signal that ticks at a fixed rate (a 3
  GHz clock ticks 3 billion times per second); each tick paces the CPU's
  fetch-decode-execute cycle, and "clock speed" is the everyday name for
  this rate.

Concept: instructions and assembly
- Know that machine code -- the only thing a CPU actually runs -- is
  nothing but numbers: every instruction (e.g. "add these two registers")
  is itself encoded as one or more bytes with a specific numeric meaning
  the CPU's decode step understands.
- Know that assembly language is the human-readable spelling of those
  same numbers: a short mnemonic (memorable abbreviation, e.g. `mov` for
  "move a value", `add` for "add") stands in for one specific machine
  code instruction, in a strict one-to-one correspondence. Each
  individual instruction does exactly one tiny thing -- move a value,
  add two registers, compare two values, jump to a different
  instruction -- nothing more.
- Know that different CPU families understand different instruction
  sets (the specific vocabulary of numeric instructions a given CPU
  design supports) -- an instruction's numeric encoding on one CPU family
  can mean something completely different, or nothing at all, on another.
- Concrete cross-platform example, "add two numbers, store in a
  register": on x86-64 (the instruction set family used by most Intel
  and AMD desktop/laptop CPUs), this looks like:
  ```
  mov eax, 5      ; put the value 5 into register eax
  add eax, 3      ; add 3 to eax, so eax now holds 8
  ```
  On ARM64 (the instruction set family used by Apple Silicon Macs and
  most phones), the same operation looks like:
  ```
  mov w0, #5      ; put the value 5 into register w0
  add w0, w0, #3  ; add 3 to w0, so w0 now holds 8
  ```
  Both do exactly the same arithmetic, but the register names (`eax` vs.
  `w0`), the instruction spellings, and the raw numeric encodings
  underneath are entirely different -- there is no shortcut translation
  between them at the byte level.
- Know that this is exactly why a compiled program must be compiled
  separately for each CPU family it will run on: a program built into
  x86-64 machine code contains x86-64 instruction bytes, which an ARM64
  CPU's decode step cannot understand at all (they are not "wrong
  answers," they decode to different, likely nonsensical, instructions).
  This is why a compiled app built for an Apple Silicon (ARM64) Mac
  cannot run on an Intel (x86-64) PC, and vice versa, without being
  recompiled or translated (this ties directly into the compiling
  process covered in row 4, Command-Line & Compilation, where the
  compiler is the program that performs this per-platform translation).

Concept: how C++ relates to all of this
- Know that a single, ordinary-looking C++ statement expands into several
  machine instructions. `int c = a + b;` becomes, roughly: load `a` from
  memory into a register, load `b` from memory into another register, add
  the two registers together, and store the result into `c`'s memory
  location -- the exact load-operate-store pattern described above, just
  issued automatically rather than hand-written.
- Know that the compiler is the program responsible for this translation
  end to end: it reads human-written C++ source and produces the
  platform-specific machine code (row 4 covers the compiler and the
  compile/link pipeline in full detail) -- this is the same reason a
  compiled C++ program, like any compiled program, must be built
  separately for each target CPU family.

Concept: where a running program lives in memory
- Know that both a program's code (its compiled instructions) and its
  data (its variables) live in memory at the same time while it runs --
  there is no separate "instruction-only" hardware; code is just bytes in
  memory like anything else, sitting at a location the CPU is told to
  execute from.
- Know the program counter (PC) is a special-purpose register that always
  holds the memory address of the next instruction to fetch; each
  fetch-decode-execute cycle reads the instruction at the address the PC
  currently points to, then normally advances the PC to the next
  instruction's address (or, for a jump/branch instruction, sets the PC
  to some other address entirely -- this is how loops and function calls
  work under the hood).
- Preview, the stack and the heap (full detail in row 10, Memory Model):
  a running program does not just have one undifferentiated blob of data
  memory -- it organizes its variables into distinct regions with
  different lifetimes and management rules, most importantly a stack
  (fast, automatically-managed, tied to function calls) and a heap
  (manually managed, lives until explicitly freed). Nothing about that
  split is visible yet from what this lecture has covered; it is simply
  more structure layered on top of "memory is a row of bytes."
- Preview, why types matter (full detail in rows 5 and 19, the latter
  including the union-dissector activity): since memory is just raw
  bytes with no attached label saying "this is an int" or "this is a
  float," a C++ type is entirely the compiler's and the running
  program's agreement about how many bytes a value occupies and how to
  interpret those bytes' numeric pattern (as a whole number, as a
  fraction, as a character, etc.). The exact same 4 bytes can be read as
  a completely different value depending on which type is used to
  interpret them -- this is precisely what row 19's union-dissector
  activity demonstrates directly.
- Preview, why the operating system exists (full detail in row 15, Basic
  OS Theory): a running program does not get to touch real hardware
  memory addresses or the real disk directly on its own -- the operating
  system sits between every program and the physical hardware, handing
  out and protecting memory, mediating file access, and giving each
  program the illusion that it has the machine to itself.

Concept: mental models later rows quietly assume
- Know that everything in memory has an address, and a value can be
  found, passed around, and stored purely by knowing that address --
  this is the entire basis for pointers (row 11), which is nothing more
  than "a variable whose value is itself an address."
- Know that memory is finite: a real machine has a fixed, limited number
  of bytes of RAM, and a program that keeps allocating memory without
  ever releasing it will eventually exhaust that supply -- this is the
  practical stakes behind memory leaks and the profiling tools covered in
  row 26.
- Know, as one honest paragraph, that CPUs have gotten dramatically
  faster than memory over the decades: a CPU can execute many
  instructions in the time a single trip to main memory takes to
  complete. To hide this gap, real CPUs contain caches -- small pools of
  very fast memory, physically closer to the CPU than main RAM, that
  automatically keep a copy of recently- and nearby-used data. Because of
  how caches work, accessing memory in a predictable, nearby pattern
  (locality) is dramatically faster in practice than jumping around
  memory unpredictably, even though both are "just" reading from RAM as
  far as the C++ source code is concerned. This single fact motivates
  row 19's Struct of Arrays vs. Array of Structs comparison (dod-hot-cold)
  and row 29's discussion of data structure locality.

## Study checklist

- [ ] Explain, using the mailbox-street analogy, what an address is and
      what a byte holds.
- [ ] Show the two bytes that store the text "Hi" and explain why the
      number 300 cannot fit in a single byte.
- [ ] Convert a byte value between decimal, binary, and hexadecimal (e.g.
      72, 0100 1000, 0x48) by hand.
- [ ] Explain why hardware uses binary physically, and why hex exists as
      a notation rather than a hardware feature.
- [ ] Explain what a register is, why it is faster than memory, and the
      load-operate-store pattern the CPU must use to work with a value
      that starts out in memory.
- [ ] State the three steps of the fetch-decode-execute cycle and what
      the clock does.
- [ ] Explain the difference between machine code and assembly, and show
      the same "add 5 and 3" operation in both x86-64 and ARM64 assembly.
- [ ] Explain why a program compiled for one CPU family will not run on
      another, and connect this to why compilation happens per platform.
- [ ] Trace `int c = a + b;` into its load/add/store instruction shape.
- [ ] Explain what the program counter register does.
- [ ] State, in one sentence each, what rows 10, 5/19, and 15 add on top
      of this lecture's model of memory, types, and the OS.
- [ ] Explain, in one paragraph, why caches exist and why locality
      matters, even though this lecture has not yet covered any specific
      data structure.

## Practiced in

none -- lecture only
