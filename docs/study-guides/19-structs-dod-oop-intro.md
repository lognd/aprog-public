# Study Guide 19: Structs (DOD & OOP intro)

This module covers user-defined value types before classes proper: enums
(scoped and unscoped), unions and type punning, struct padding and
alignment, and data-oriented design (AoS vs SoA and the CPU cache). The
capstone assignment maps a real binary image format (TGA) onto a packed
struct and processes pixels through it.

## Know before you start

- `sizeof` and byte-level reasoning about primitive types [assumed: row 5
  -- Variables & Type]
- Binary file reading with `std::ios::binary`, `seekg`, and little-endian
  byte order [assumed: row 16 -- Streams & Files]
- `argc`/`argv` parsing and validation [assumed: row 14 -- Command Line
  Arguments]
- Row-major flat storage of 2D data [assumed: row 11 -- Pointers]

## Taught here

Concept: enums
- Know that an `enum` gives names to a group of related integer constants,
  replacing unreadable magic numbers; the compiler assigns values starting
  at 0 unless explicit values are given.
- Know that unscoped `enum` values implicitly convert to `int`, which is
  convenient but dangerous (they can silently mix with plain integers and
  other enums).
- Know that `enum class` (a scoped enum, C++11) forbids implicit
  conversion: extracting the underlying integer requires an explicit
  `static_cast<int>`, and values must be written with their qualified name
  (`Color::Red`).
- Know that `sizeof` an `enum` and an `enum class` are typically the same
  -- scoping changes type checking, not storage.
- Know the C idiom `typedef enum { ... } Name;` and that C++ does not
  require it because enum names are usable directly as types.
- Be able to write an exhaustive `switch` over an `enum class` with one
  case per possible value.

Concept: unions and type punning
- Know that a `union` declares one block of memory accessible through any
  of its named members: all members share the same starting address and
  bytes, so `sizeof(union)` equals the size of its largest member, not the
  sum.
- Know the three union use cases: saving space among mutually exclusive
  fields, type punning (inspecting one type's raw bytes as another type),
  and discriminated (tagged) unions.
- Know the C vs C++ split: reading a union member you did not write is
  defined behavior in C (C11 6.5.2.3) but undefined behavior in C++ due to
  the strict aliasing rule (the compiler may assume pointers of different
  types never alias, and optimize accordingly).
- Know the safe C++ alternatives for type punning: `std::memcpy` into the
  target type (C++11, optimized to a register move) and `std::bit_cast`
  (C++20).
- Know that a discriminated union pairs a union with an enum tag recording
  which member is active; reading only the member last written is
  well-defined in both languages, and forgetting the tag is entirely the
  programmer's risk.
- Know the type-theory framing: a struct is a product type (holds ALL its
  fields simultaneously), a sum type holds EXACTLY ONE of its variants at
  a time, a raw union is an unsafe sum type, and `std::variant` (C++17) is
  the safe, tag-carrying version that throws on wrong-variant access.
- Know that IEEE 754 gives `1.0f` the bit pattern `0x3f800000` and `-0.0f`
  the pattern `0x80000000`, and that on little-endian machines those bytes
  appear low-byte-first in memory.

Concept: struct padding and alignment
- Know that natural alignment means each type prefers a starting address
  divisible by its own size (4-byte `int` at a multiple of 4, 8-byte
  `double` at a multiple of 8), because the CPU's memory bus reads whole
  words at a time.
- Know that a misaligned access is transparently fixed (but slower) on
  x86, and can be a hardware fault on stricter architectures.
- Know that the compiler inserts invisible padding bytes between struct
  fields to keep each field naturally aligned, and pads the struct's total
  size to a multiple of its largest member's alignment so arrays of it
  stay aligned.
- Be able to predict a struct's layout on paper -- field offsets, padding
  locations, and total `sizeof` -- and verify with the `offsetof` macro.
- Know that `#pragma pack(push, 1)` saves the current packing setting and
  switches to 1-byte alignment (no padding), and that `#pragma pack(pop)`
  restores it; forgetting the `pop` silently packs every struct defined
  afterward, a hard-to-trace bug.
- Know that reordering fields largest-first reduces padding while keeping
  natural alignment -- a middle ground between the default and full
  packing.
- Know that packed structs are required when mapping binary file formats,
  network packets, or hardware registers, where the on-disk byte offsets
  are fixed and admit no padding.

Concept: data-oriented design (the memory wall)
- Know that fetching a value from RAM costs roughly 100-300 ns (~300
  cycles at 3 GHz) while the CPU can execute hundreds of instructions in
  that time -- this gap is the "memory wall."
- Know that the CPU cache is a small, very fast on-chip memory that holds
  recently fetched 64-byte blocks (cache lines), serving hits in 1-4
  cycles instead of ~300.
- Know that sequential access (spatial locality) yields near-100% cache
  hit rates because fetching one element brings its neighbors along, while
  large random jumps yield near-0% hit rates.
- Know the Array of Structs (AoS) problem: when a loop touches only a few
  hot fields of a wide struct, every cache line fetched is mostly cold
  bytes (fields the loop never uses), wasting cache capacity.
- Know the Struct of Arrays (SoA) layout: each field in its own flat
  array, so a loop over one field reads perfectly contiguous memory with
  no interleaved cold data.
- Know the hot-cold split principle: store fields that are used together
  in the same loops together in memory, and know the trade-off -- SoA is
  measurably faster for partial-field loops (typically 2-5x in the
  benchmark) but less readable, so real codebases use AoS by default and
  switch only for critical hot loops.
- Be able to convert a small AoS program to SoA by hand.

Concept: binary image processing over a packed struct
- Be able to map the 18-byte TGA header onto a `#pragma pack(1)` C++
  struct so `fread`/`ifstream::read` fills the fields at the correct byte
  offsets, and know that without packing `sizeof(TGAHeader)` exceeds 18
  and the read lands on wrong bytes.
- Know that TGA stores pixels as 3 bytes in Blue-Green-Red order (not
  RGB), rows bottom-first, and that all multi-byte header fields are
  little-endian -- which "just works" on little-endian hosts by
  coincidence, not by checked correctness.
- Be able to implement per-channel pixel operations with correct clamping
  to [0, 255], doing arithmetic in a wider integer type before clamping:
  multiply, screen, subtract, and overlay blend modes, channel add/scale,
  channel combine, and vertical flip (reverse row order).
- Be able to parse a variadic CLI argument list, validating each operation
  name and its arguments in order.

## Study checklist

- [ ] Explain the safety difference between `enum` and `enum class`.
- [ ] State when reading an unwritten union member is defined and when it
      is undefined, and name the two safe C++ alternatives.
- [ ] Draw the padded layout of a `char, int, char, double` struct and
      compute its `sizeof`.
- [ ] Explain what forgetting `#pragma pack(pop)` does.
- [ ] Explain why SoA beats AoS for a loop touching two fields of a
      ten-field struct.
- [ ] Explain why `#pragma pack(1)` is mandatory for the TGA header
      struct.

## Practiced in

`enum-field-day`, `union-dissector`, `struct-layout-bingo`, `dod-hot-cold`, `tga-processor`
