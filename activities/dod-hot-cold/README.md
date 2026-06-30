# Activity: DOD Hot-Cold Split

Your CPU is extraordinarily fast -- it can execute billions of simple
operations per second. RAM is extraordinarily slow by comparison. Fetching
one value from RAM can take 100-300 nanoseconds, which is time the CPU could
have spent executing hundreds of arithmetic instructions instead. This gap is
called the "memory wall," and it is one of the most important practical
constraints in systems programming.

This activity runs two particle-simulation benchmarks that perform identical
work -- the same number of particles, the same number of iterations, the same
arithmetic -- but arrange data differently in memory. One is measurably slower.
You will observe the difference, learn why it happens, and then perform the
same transformation yourself on a small program.

## Background

### RAM is slow, and the CPU is fast

When your program does `int x = arr[i]`, the CPU cannot operate on `arr[i]`
until it has been fetched from RAM. Fetching takes time -- on modern hardware,
roughly 100 ns, which at 3 GHz translates to ~300 clock cycles of waiting
with nothing to do. A tight loop that fetches a new random location from RAM
on every iteration is actually spending almost all of its time waiting, not
computing.

### The hardware's secret shortcut: spatial locality

CPU designers noticed that programs have a strong tendency to access memory
in order. If you just read `arr[0]`, you will probably read `arr[1]` next,
then `arr[2]`, and so on. So the hardware does not fetch just one value when
you ask for one -- it secretly fetches a block of about 64 consecutive bytes
(called a "cache line") and stores them in a small, extremely fast memory
called the **cache** (pronounced "cash"). The cache is built into the CPU chip
itself, not on a separate RAM chip, and it can serve a value in 1-4 clock
cycles instead of 300.

If the next value your program needs is already in the cache from a previous
fetch, it arrives almost instantly. If it is not in the cache, the CPU must
go to RAM, paying the full 300-cycle penalty. The percentage of accesses that
hit the cache is called the **cache hit rate**, and it dominates the
performance of memory-intensive programs.

Accessing memory in sequential order -- reading `arr[0]`, then `arr[1]`, then
`arr[2]` -- is called **sequential access** or exploiting **spatial locality**.
It produces near-100% cache hit rates because after fetching `arr[0]`, the
cache already holds `arr[1]` through `arr[15]` (assuming 4-byte ints). The
next 15 accesses are free.

Accessing memory in large random jumps -- reading `arr[0]`, then `arr[100]`,
then `arr[7]` -- produces near-0% cache hit rates because each access is to a
location not in the cache. Every access pays the full 300-cycle penalty.

### Array of Structs: the interleaving problem

Suppose you have a particle with many fields:

```cpp
struct Particle {
    float x, y, z;      // position  -- 12 bytes
    float vx, vy, vz;   // velocity  -- 12 bytes
    float r, g, b, a;   // color     -- 16 bytes
    float mass;          // mass      --  4 bytes
    char  name[16];      // debug name -- 16 bytes
};
Particle particles[N];
```

`sizeof(Particle)` is 60 bytes. Your physics update loop only touches
`x`, `y`, `z`, `vx`, `vy`, `vz` -- 24 bytes per particle. But when the cache
fetches a 64-byte block starting at `particles[0].x`, it picks up all 60 bytes
of particle 0 and the first 4 bytes of particle 1. Of those 64 bytes, only 24
are the position and velocity fields you actually need. The other 40 bytes
(color, mass, name) are wasted -- they fill cache slots that could have held
position data for particles 2 and 3. Those particles now must wait for a fresh
fetch from RAM.

In an Array of Structs (AoS), all the hot data (frequently accessed) and
cold data (rarely accessed) are interleaved together. Every cache fetch pulls
in cold bytes that are never used in the current loop.

### Struct of Arrays: packing hot data together

The Struct of Arrays (SoA) layout stores each field in its own flat array:

```cpp
float xs[N];   float ys[N];   float zs[N];
float vxs[N];  float vys[N];  float vzs[N];
float rs[N];   float gs[N];   float bs[N];   float as[N];
float masses[N];
char  names[N][16];
```

Now when the cache fetches a 64-byte block starting at `xs[0]`, it loads
`xs[0]` through `xs[15]` -- 16 floats, all of them the x-positions of 16
particles. The next 15 loop iterations are already in the cache. There is no
interleaved cold data, no wasted space. The cache hit rate approaches 100%.

The physics update loop in SoA form:

```cpp
for (int i = 0; i < N; ++i) {
    xs[i] += vxs[i];
    ys[i] += vys[i];
    zs[i] += vzs[i];
}
```

reads six contiguous arrays, each accessed perfectly sequentially. The memory
access pattern is as cache-friendly as possible.

### The hot-cold split

The core insight is to separate **hot fields** (those your tight loops touch
every iteration) from **cold fields** (those accessed rarely, such as color
or a debug name). In the SoA layout, the physics update loop never touches the
color or name arrays at all -- they are physically separate in memory and do
not pollute the cache during the update.

This is called a **hot-cold split**: organize data so that the fields used
together in the same loops are stored together in memory.

### The trade-off

SoA code is less readable than AoS. `particle.x` is more natural than
`xs[particle_index]`. Passing a single particle around means passing six
indices or six pointers. Most real codebases use AoS for code clarity and only
switch to SoA for the specific hot loops where performance is critical.

Before writing any struct, ask: what will my innermost loops do with this
data? What fields will those loops touch? If only a subset of fields are hot,
consider whether separating them into their own arrays is worth the added
complexity.

## Concepts covered

- Sequential memory access and spatial locality
- The CPU cache: what it is, why it exists, and when it helps
- Array of Structs (AoS) layout and its cache inefficiency for partial-field loops
- Struct of Arrays (SoA) layout and why it improves cache utilization
- Hot-cold data splitting as a performance technique
- Converting an AoS program to SoA by hand

## How it works

The workspace contains two pre-built benchmarks (`aos_bench` and `soa_bench`)
and one source file you must modify (`rewrite_me.cpp`).

Both benchmarks update the position of 2 million particles 10 times. The only
difference is how the particles are stored in memory. Run them, compare the
times, and read this README to understand the result.

Then open `rewrite_me.cpp`. It contains an AoS implementation using
`struct Vec2 { int x; int y; }` that intentionally does not compile. Your
job is to delete the AoS code and replace it with SoA code (two separate
arrays, `xs[1000]` and `ys[1000]`) that computes the same sum and prints the
same output. The comment at the top of the file explains exactly what to do.

When you run `./rewrite_me` and it prints `sum_x: 499500`, the launcher
will capture that output and unlock the passphrase.

## Getting started

```bash
python3 launch.py
```

A shell opens inside a fresh copy of the activity workspace.

### Step 1 -- build and run the AoS benchmark

```
make
./aos_bench
```

Write down the time printed (in milliseconds).

### Step 2 -- run the SoA benchmark

```
./soa_bench
```

Write down the time. Compute the ratio: AoS time divided by SoA time. On most
machines this is between 2x and 5x faster for SoA.

### Step 3 -- read the background section of this README

If you have not read the Background section above, read it now before
continuing. Use `less README.md` inside the shell (press `q` to quit).

### Step 4 -- convert rewrite_me.cpp to SoA

Open `rewrite_me.cpp` in a text editor. Follow the instructions in the
comments at the top of the file. The rules are:

1. Delete the `static_assert` line.
2. Remove the `struct Vec2` definition.
3. Declare `int xs[1000];` and `int ys[1000];` as separate arrays.
4. Initialize: `xs[i] = i; ys[i] = 0;` for `i` in `0..999`.
5. Compute `sum_x` by summing all `xs[i]` values.
6. Print exactly: `printf("sum_x: %d\n", sum_x);`

### Step 5 -- build and verify

```
make rewrite_me
./rewrite_me
```

The output should be exactly: `sum_x: 499500`

### Step 6 -- exit

```
exit
```

The launcher builds and runs your `rewrite_me` automatically, checks the
output, and reveals the passphrase if it matches.

## You will know you are done when...

The launcher prints `Passphrase:` followed by the passphrase after you type
`exit` in the shell.

## Hints

<details>
<summary>Hint 1 -- what sequential access means and why it matters</summary>

When you loop over `xs[0], xs[1], xs[2], ...`, each access is exactly 4 bytes
past the previous one. The cache fetches a 64-byte block at a time, so after
reading `xs[0]`, the cache already holds `xs[0]` through `xs[15]`. The next
15 iterations are served from the fast cache without going to RAM.

When you loop over `particles[0].x, particles[1].x, particles[2].x, ...`,
each x-position is 60 bytes past the previous one (the full struct size). The
cache fetches `particles[0]` (all 60 bytes), but you only use 4 bytes (x).
The next fetch for `particles[1].x` may require a new trip to RAM because it
is 60 bytes away and may not be in the same 64-byte block.

The rule: if your loop only needs a few fields, store those fields
contiguously in their own array.

</details>

<details>
<summary>Hint 2 -- how to convert AoS to SoA</summary>

Replace this AoS code:

```cpp
struct Vec2 { int x; int y; };
Vec2 points[1000];
for (int i = 0; i < 1000; ++i) { points[i].x = i; points[i].y = 0; }
int sum_x = 0;
for (int i = 0; i < 1000; ++i) { sum_x += points[i].x; }
```

With this SoA code:

```cpp
int xs[1000];
int ys[1000];
for (int i = 0; i < 1000; ++i) { xs[i] = i; ys[i] = 0; }
int sum_x = 0;
for (int i = 0; i < 1000; ++i) { sum_x += xs[i]; }
```

Then print: `printf("sum_x: %d\n", sum_x);`

</details>

<details>
<summary>Hint 3 -- why sum_x should equal 499500</summary>

`xs[0] + xs[1] + ... + xs[999]` is `0 + 1 + 2 + ... + 999`.

The formula for the sum of the first N non-negative integers is `N * (N-1) / 2`.
For N = 1000: `1000 * 999 / 2 = 499500`.

If your program prints a different number, check that you are summing `xs[i]`
(not `ys[i]`, which are all zero) and that the initialization sets `xs[i] = i`.

</details>

## Going further

- Modify `aos_bench.cpp` to also measure only the memory reads (no position
  update) and compare that time to the position-update time. Does the read-only
  loop show the same AoS vs SoA gap?
- Add a `rand_bench.cpp` that stores positions in random memory locations
  (using `new float` for each particle individually) and compare its speed to
  both AoS and SoA. This is the worst case for the cache.
- Read about the "cache line" size on your machine:
  `getconf LEVEL1_DCACHE_LINESIZE`. How many floats fit in one cache line?
  How does that number relate to the speedup you observed?
- Look up "structure of arrays" and "AoS vs SoA" in the context of SIMD
  (Single Instruction Multiple Data). Modern CPUs can add 8 floats
  simultaneously if they are contiguous -- SoA is required to take advantage
  of this.
