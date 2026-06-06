# Vector Inspector & Corrector

A `std::vector` stores its elements in a block of memory called a buffer.
As you add elements with `push_back`, the vector occasionally needs more
room.  When that happens it allocates a brand-new buffer, copies every
existing element into it, and frees the old one.  This is called a
**reallocation**.

The program in this activity is causing more reallocations than necessary.
Your job is to figure out why and fix it.

## Getting started

    python3 launch.py

A shell opens inside a fresh copy of the project.

## Walk-through

### Step 1 -- compile and run the program

    make && ./inspector

The program adds 8 values to a vector one at a time and prints a table.
The column labelled `data-address` shows where the vector's buffer is
sitting in memory.  Every time you see `<-- buffer moved!` the vector
reallocated: it found a new address, copied everything over, and moved on.

Look at how many times that happens and think about whether it should be
happening that often.

### Step 2 -- read the documentation

The program uses `reserve`.  Read what it does and, crucially, what the
**Notes** section says about when and how it should be called:

> https://en.cppreference.com/cpp/container/vector/reserve

Come back once you have a theory about what is going wrong.

### Step 3 -- fix main.cpp

Open `main.cpp`, apply your fix, recompile, and run again:

    make && ./inspector

### Step 4 -- exit

    exit

The launcher will check your work automatically and reveal the passphrase.

## You'll know you're done when...

The table shows zero `<-- buffer moved!` entries.

## Why does this matter?

Every time a vector reallocates, any pointer or reference you had saved into
its elements becomes invalid -- it points to memory that was already freed.
This kind of bug is very hard to track down.

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
