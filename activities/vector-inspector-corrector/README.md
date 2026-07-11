# Activity: Vector Inspector & Corrector

A `std::vector` stores its elements in a block of memory called a buffer.
A vector tracks two separate numbers: its **size** (how many elements it
currently holds) and its **capacity** (how many elements the current buffer
has room for before it runs out of space).  As you add elements with
`push_back`, size grows toward capacity.  Once size would exceed capacity,
the vector needs more room: it allocates a brand-new, bigger buffer, copies
every existing element into it, and frees the old one.  This is called a
**reallocation**.

The program in this activity is causing more reallocations than necessary.
Your job is to figure out why and fix it.

## Concepts covered

- `std::vector` internal buffer: capacity vs. size and how they differ
- Reallocation: when the buffer is full, the vector allocates a new one and copies everything
- `reserve`: pre-allocating capacity to prevent reallocation during a known-size insertion loop
- Why a reallocation makes the vector's old buffer address stale: anything that remembers where an element used to live can end up wrong after the buffer moves

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the project.

### Step 1 -- compile and run the program

```bash
make && ./inspector
```

The program adds 8 values to a vector one at a time and prints a table.
The column labelled `data-address` shows where the vector's buffer is
sitting in memory.  Every time you see `<-- buffer moved!` the vector
reallocated: it found a new address, copied everything over, and moved on.

Look at how many times that happens and think about whether it should be
happening that often.

### Step 2 -- read the documentation

The program uses `reserve`, which asks the vector to grow its buffer's
capacity to at least a given number of elements right away, without
changing its size or adding any elements.  Read what it does and,
crucially, what the **Notes** section says about when and how it should
be called:

> https://en.cppreference.com/cpp/container/vector/reserve

Come back once you have a theory about what is going wrong.

### Step 3 -- fix main.cpp

Open `main.cpp`, apply your fix, recompile, and run again:

```bash
make && ./inspector
```

### Step 4 -- exit

```
exit
```

The launcher will check your work automatically and reveal the passphrase.

## You will know you are done when...

The table shows zero `<-- buffer moved!` entries.

Every time a vector reallocates, any address you had saved for one of its
elements becomes stale -- it refers to memory that was already freed. If
your program had that old address written down somewhere, using it would
read or write freed memory. This kind of bug is very hard to track down,
and it is one of the main reasons later material on pointers and iterators
spends so much time on "invalidation" rules for each container.

## Hints

<details>
<summary>Hint 1 -- what to look for in the Notes section</summary>

The Notes section on cppreference explains the relationship between
`reserve`, capacity, and when reallocation is triggered.  Pay attention
to how often `reserve` is being called in the loop and what argument it
receives each time.

</details>

<details>
<summary>Hint 2 -- where to make the change</summary>

`reserve` should be called once, before the loop, with the total number
of elements you plan to add -- not once per iteration with a growing count.

</details>

## Going further

- After fixing `reserve`, save a pointer to `vec[0]` before the loop and
  check whether it still points to the same element after the loop. Is it
  still valid?
- Look up `std::vector::shrink_to_fit`. When would you call it, and does it
  guarantee anything?
- Compare `push_back` (which may reallocate) with `emplace_back`. Under what
  circumstances does `emplace_back` avoid an extra copy?
