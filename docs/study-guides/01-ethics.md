# Study Guide 1: Ethics

This module is about the responsible use of AI coding assistants. Instead of
teaching a new C++ or Python concept, it asks you to experience firsthand what
happens when you ship code you do not understand -- a class of AI-assisted
"vibe coding" -- so that you build a healthy skepticism toward code-generation
tools before you rely on them in later, harder assignments.

## Know before you start

- Basic C++ class syntax: constructors, destructors, member functions
  [assumed: GAP -- no earlier row teaches C++ class syntax; this assignment
  is sequenced before the OOP rows that introduce it]
- What a dynamic array (heap-allocated, resizable buffer) is conceptually
  [assumed: GAP -- taught properly in row 10 (Memory Model) and row 25
  (Dynamic Memory), both later than this row]

## Taught here

Concept: AI-assisted coding and its risks
- Know that "vibe coding" means generating code with an AI assistant and
  shipping it without fully understanding how it works.
- Know that AI-generated code can compile and look plausible while still
  containing semantic bugs (wrong function called), logical bugs (wrong
  loop bound or type), and resource-management bugs (leaks, shallow
  copies, dangling pointers).
- Be able to read AI-generated or AI-assisted code line by line and
  identify which lines you do not understand before accepting them.
- Know that relying on code generation without understanding it creates a
  long-term skill gap that compounds in later, harder coursework and jobs.

Concept: bug classes exercised by the broken starter code
- Know that a missing access specifier at the top of a C++ class body
  makes every member private by default, which can silently break code
  that expects public access.
- Know that a copy constructor must allocate its own buffer and copy
  element values, not just copy the pointer, or two objects end up
  sharing (and later double-freeing) the same heap memory.
- Know that a move constructor should take an rvalue reference (`Type&&`),
  not a `const Type&&`, because a `const` rvalue reference cannot have its
  members transferred out.
- Know that copy and move assignment operators must return a reference to
  `*this` so that chained assignment (`a = b = c;`) works.
- Know that a resizing routine (like `push_back`) must handle the
  zero-capacity case explicitly (for example, growing from 0 to 1) before
  doubling, or the size never grows from zero.

## Study checklist

- [ ] Explain in your own words why shipping AI-generated code you do not
      understand is risky in a course designed to teach you to program.
- [ ] Given a class with copy/move constructors and assignment operators,
      identify which ones are shallow-copying a pointer instead of
      transferring ownership correctly.
- [ ] Explain why a resizing/growth routine needs a special case for zero
      capacity.

## Practiced in

`ai-vector-i`

## Gaps detected

- C++ class syntax (constructors, destructors, member access) is assumed
  by `ai-vector-i` but not taught by any earlier row. [assumed: GAP]
- The concept of heap-allocated dynamic arrays and ownership is assumed
  but not formally taught until row 10 / row 25, both later. [assumed: GAP]
