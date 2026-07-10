# Course Cohesion Reference

The curriculum should feel unified: concepts introduced once, called back
to by name, and built on -- not re-explained in parallel vocabularies.
This file is the registry of canonical cross-references and voice rules.
When adding or editing content, reuse these chains; do not invent
parallel ones.

## Canonical callback chains

- Mailbox-street memory model (row 3) -> addresses (row 11 pointers) ->
  the fd table lives in the kernel (row 15) -> cache locality (rows 19, 29).
- The row-12 mystery: std::string == compares contents, char* == compares
  addresses -> resolved by operator-overload-workshop (row 21).
- The syscall doorbell: write-your-first-syscalls (row 15) ->
  os-mental-models names it -> raii-file-guard wraps it (row 21) ->
  hex-dump uses it in anger.
- The complexity taste (row 6, informal: "double the input, four times
  the wait") -> formal notation only at row 28.
- The fix ladder: comments -> RAII (row 21) -> smart pointers (row 27) ->
  Rust refuses to compile it (row 60). Ownership = release exactly once
  (row 25).
- The space between the lines: partially-formed objects (row 24) <->
  virtual-in-ctor (row 22) <-> ctor-establishes-invariants (row 21).
- Sum types: union-dissector (row 19) -> invalid-states-unrepresentable
  (row 24) -> Option/Result in other languages (row 60).
- Build-then-meet-std: linked-list-from-scratch (row 30) -> std::list
  (row 32); deque-two-ways (row 31) -> std::deque; MyUniquePtr (row 27)
  -> std::unique_ptr; your insert_after (row 35) -> forward_list's
  (row 32).
- Event loop family: SFML game loop (row 41) <-> asyncio (row 55) --
  same concept, different costume; interrupts stay in the extra-depth
  layer (row 55's who-handles-the-wait README).
- The ledger domain: tiny-ledger-api (Flask, hand-validated) ->
  typed-ledger-api (FastAPI, types validate) -- same domain on purpose
  so the improvement is the only variable.

## Voice rules

- Beginner-first always (docs/readme-style.md): define every term at
  first use; concrete before abstract.
- Motivate before you mechanize: show the pain (legacy rot, the bug the
  design permits) before the fix.
- Honesty questions are part of the voice: sometimes the answer is "just
  use std::sort" or "no pattern needed".
- Passphrases restate the lesson as a small joke
  (a-branch-is-just-a-pointer, the-clock-decides-not-you); keep the
  tradition.
