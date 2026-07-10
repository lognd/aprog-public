# Activity: Link Tracer

A singly linked list is built from individual nodes -- small heap-allocated
structs holding a value and a pointer to the next node -- wired together by
hand. This activity works directly with a minimal `Node` struct (`int
data; Node* next;`) and raw pointers, no `std::list` and no smart pointers,
so you can see exactly what each classic manipulation (inserting,
deleting, reversing, finding the middle) does to the chain of pointers, one
step at a time.

## Background

Every program in this activity manages its own `Node*` pointers with plain
`new` and `delete`, the same way `std::list` is built underneath. This is
deliberate: a `next` pointer wrapped in a smart pointer would recursively
destroy the whole chain one destructor call at a time (risking a stack
overflow on a long list) and would hide exactly the pointer mechanics this
activity exists to teach. You already practiced smart pointers elsewhere in
this course -- here the goal is to see the raw next-pointer machinery
directly, matching the mental model used in the companion "Linked List From
Scratch" assignment.

## Concepts covered

- The node/next-pointer chain: `push_front`, `insert_after` (linking a new
  node in without losing the rest of the chain)
- Relinking around a removed node (`delete_middle`) without leaking or
  reading freed memory
- Reversing a list in place with three pointers (`prev`, `cur`, `next`)
- Finding the middle of a list in one pass with a slow pointer and a fast
  pointer (the "tortoise and hare" technique)
- Diagnosing a broken relink: what happens to a node's memory when a
  pointer update happens in the wrong order and a node becomes unreachable

## How it works

Each of the six snippets shows a complete, compilable C++ program that
builds a small list and performs one manipulation on it. Read the code,
trace through it by hand, and type the exact output it prints -- for
multi-line output, you will be prompted to enter one line at a time. The
launcher compiles and runs each program itself and checks your prediction
against the real, measured output. Predict every snippet correctly to
reveal the passphrase.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

You have correctly predicted the output of all six snippets and the
launcher prints the activity's passphrase.

## Hints

<details>
<summary>Hint 1 -- always save next before you delete or overwrite</summary>

The recurring trap in several of these snippets is touching a node's
`next` pointer (by deleting the node or by overwriting a pointer to it)
before something else that needs the OLD value has read it. Whenever you
see a `delete` or a pointer reassignment, ask: does anything downstream
still need the value this is about to destroy?

</details>

<details>
<summary>Hint 2 -- draw the chain after every statement</summary>

For the reverse and find-middle snippets especially, draw small boxes for
each node and redraw the arrows after every line that touches a pointer.
Trying to hold the whole chain in your head at once is where mistakes
creep in.

</details>

## Going further

- Extend the reverse snippet to reverse only the first `k` nodes of a
  longer list, leaving the rest of the chain untouched.
- Modify the broken-relink snippet (snippet 6) to actually fix the bug --
  save the pointer before overwriting it -- and confirm the list comes out
  as `10 99 20 30`.
- Write your own snippet that builds a list, intentionally introduces a
  cycle, and detects the cycle using the same slow/fast pointer technique
  from the find-middle snippet (a fast pointer will eventually equal the
  slow pointer if and only if there is a cycle).
