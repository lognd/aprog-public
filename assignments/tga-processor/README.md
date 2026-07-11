# TGA Image Processor

The TARGA (TGA) file format is one of the simplest image formats ever designed.
No compression, no metadata layers, no codec negotiation -- just an 18-byte header
followed by raw pixel data stored directly as bytes. That simplicity is exactly
what makes it a great first binary file format to implement: you can map the header
directly onto a C++ struct, read it in one `fread`, and start processing pixels
immediately.

In this assignment you will build a command-line image processing tool that reads
TGA files, applies a sequence of operations (blending, color adjustment, geometric
transforms), and writes the result to a new TGA file. Every operation you implement
works at the level of individual pixels -- you will feel, concretely, how image
editing software like Photoshop or GIMP works at its core.

---

## Learning goals

- Map a binary file format onto a packed C++ struct using `#pragma pack`
- Read and write raw binary data using `fread` / `fwrite` or `ifstream` in binary mode
- Parse a variadic command-line argument list and validate each argument in order
- Implement mathematical blend modes and color operations with correct clamping
- Understand how an array of structs represents a 2D image and how to traverse it

---

## Background: the TGA format

A TGA file is laid out as follows:

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| 0 | 1 | `idLength` | Length of image ID field (usually 0) |
| 1 | 1 | `colorMapType` | 0 = no color map |
| 2 | 1 | `imageType` | 2 = uncompressed true-color |
| 3 | 2 | `colorMapOrigin` | Ignored when no color map |
| 5 | 2 | `colorMapLength` | Ignored when no color map |
| 7 | 1 | `colorMapDepth` | Ignored when no color map |
| 8 | 2 | `xOrigin` | X origin of image (usually 0) |
| 10 | 2 | `yOrigin` | Y origin of image (usually 0) |
| 12 | 2 | `width` | Width in pixels |
| 14 | 2 | `height` | Height in pixels |
| 16 | 1 | `pixelDepth` | Bits per pixel (24 for BGR) |
| 17 | 1 | `imageDescriptor` | Bit flags for orientation |

After the 18-byte header, pixel data follows immediately. Each pixel is stored as
3 bytes in **Blue-Green-Red** order (not RGB -- this is a quirk of the TGA format).
Pixels are stored row by row, bottom row first.

Because the header fields are packed with no padding between them (a 1-byte field
immediately followed by a 2-byte field), you must use `#pragma pack(1)` to tell the
compiler not to insert alignment padding. Without it, `sizeof(TGAHeader)` would be
larger than 18 and `fread` would overwrite the wrong bytes.

### Background: endianness and why it matters here

Fields like `width` and `height` are 2 bytes wide (`uint16_t`), but a byte can
only hold one 8-bit value. To store a number bigger than 255 in memory or in
a file, the computer splits it across two bytes and has to pick an order to
put them in. **Endianness** is the name for that ordering choice: it is a
rule for which byte of a multi-byte number is stored first.

Take the number 258. In binary that is `0000_0001 0000_0010`, which splits
into two bytes: `0x01` (the "most significant byte," worth 256) and `0x02`
(the "least significant byte," worth 2 -- together `256 + 2 = 258`). A
format has two ways to write those two bytes to disk:

- **Little-endian**: least-significant byte first -- bytes on disk are
  `02 01`.
- **Big-endian**: most-significant byte first -- bytes on disk are
  `01 02`.

TGA is a **little-endian** format: every multi-byte header field (including
`width` and `height`) is stored least-significant byte first. When you
`fread` or `ifstream::read` raw bytes straight into a `uint16_t` field of
`TGAHeader`, the CPU reassembles those bytes into a number using whatever
byte order *that CPU* uses natively. Almost every machine you will run this
assignment on (x86, x86-64, Apple Silicon in its default mode) is itself
little-endian, so this "just works" by coincidence, not because your code
checked anything. On a big-endian machine, the exact same bytes would be
reassembled in the opposite order and `width`/`height` would silently come
out wrong -- for example, a file whose `width` bytes are `02 01` (258,
little-endian) would be misread as `0x0201` = 513 on a big-endian host. The
Constraints section below requires you to detect this situation at startup
instead of silently producing corrupt output.

---

## Task

### Data structures

Define these in `src/tga.hpp`:

```cpp
#pragma pack(1)
struct TGAHeader {
    uint8_t  idLength;
    uint8_t  colorMapType;
    uint8_t  imageType;
    uint16_t colorMapOrigin;
    uint16_t colorMapLength;
    uint8_t  colorMapDepth;
    uint16_t xOrigin;
    uint16_t yOrigin;
    uint16_t width;
    uint16_t height;
    uint8_t  pixelDepth;
    uint8_t  imageDescriptor;
};
#pragma pack(pop)

struct Pixel {
    uint8_t blue;
    uint8_t green;
    uint8_t red;
};
```

`TGAHeader` must be exactly 18 bytes (`sizeof(TGAHeader) == 18`). `Pixel` must be
exactly 3 bytes. The `#pragma pack(1)` / `#pragma pack(pop)` pair ensures no padding
is inserted. Do not add or remove fields.

### File I/O

Implement `TGAImage::read(filename)` and `TGAImage::write(filename)` in `src/tga.cpp`.

`read` must:
1. Open the file in binary mode.
2. Read exactly 18 bytes into a `TGAHeader` using `fread` or `ifstream::read`.
3. Read `width * height` pixels into a `std::vector<Pixel>`.
4. Return `false` if the file cannot be opened; `true` otherwise.

`write` must write the header followed by all pixels in the same layout.

When using `ifstream`, open with `std::ios::binary`. When using `fread`, open with
`fopen(filename, "rb")`.

### CLI

Your `main.cpp` must implement the following interface:

```
./project1.out [output.tga] [input.tga] [operation] [args...]...
```

If no arguments are given, or if `--help` is passed as the first argument, print:

```
Project 1: Image Processing, <Season> <Year>

Usage:
        ./project1.out [output] [firstImage] [method] [...]
```

where `<Season>` is Spring (Jan-Apr), Summer (May-Aug), or Fall (Sep-Dec) and
`<Year>` is the current year.

Arguments are validated left to right. Stop and print an error as soon as validation
fails. Do not create the output file if any error occurs.

| Condition | Output | Exit |
|-----------|--------|------|
| Output filename does not end in `.tga` | `Invalid file name.` | non-zero |
| Input filename does not end in `.tga` | `Invalid file name.` | non-zero |
| Input file does not exist | `File does not exist.` | non-zero |
| Unknown operation name | `Invalid method name.` | non-zero |
| Operation expects argument but none given | `Missing argument.` | non-zero |
| Operation expects `.tga` argument, got non-.tga | `Invalid argument, invalid file name.` | non-zero |
| Operation expects `.tga` argument, file not found | `Invalid argument, file does not exist.` | non-zero |
| Operation expects number, got non-number | `Invalid argument, expected number.` | non-zero |

### Operations

All operations apply per-channel. Clamp all results to `[0, 255]`. Use `int` or
`float` for intermediate math to avoid overflow, then cast back to `uint8_t`.

**`multiply <file.tga>`** -- Photoshop multiply blend mode.

```
result = clamp(round((A * B) / 255.0))
```

Applied per channel (R, G, B independently).

**`subtract <file.tga>`** -- Subtract layer from base.

```
result = clamp(A - B, 0, 255)
```

**`screen <file.tga>`** -- Photoshop screen blend mode.

```
result = 255 - clamp(round(((255 - A) * (255 - B)) / 255.0))
```

**`overlay <file.tga>`** -- Photoshop overlay blend mode.

Per channel, where `base` is the current image and `blend` is the layer:

```
if base <= 127:
    result = clamp(round(2 * base * blend / 255.0))
else:
    result = 255 - clamp(round(2 * (255 - base) * (255 - blend) / 255.0))
```

**`combine <r.tga> <g.tga> <b.tga>`** -- Merge three channel images. Take the red
channel from `r.tga`, green from `g.tga`, blue from `b.tga`.

**`flip`** -- Vertical flip. Reverse the row order.

**`onlyred`** -- Set G = 0, B = 0 for every pixel.
**`onlygreen`** -- Set R = 0, B = 0 for every pixel.
**`onlyblue`** -- Set R = 0, G = 0 for every pixel.

**`addred N`**, **`addgreen N`**, **`addblue N`** -- Add integer `N` to one channel.
`N` may be negative. Clamp the result.

**`scalered N`**, **`scalegreen N`**, **`scaleblue N`** -- Multiply one channel by
float `N`. Clamp the result.

### Extra credit operations

**`blur N`** -- Gaussian blur with radius `N`. Sigma = `N / 2.0`. Build the Gaussian
kernel, apply as 2D convolution, clamp output per channel. For border pixels, clamp
the sampling coordinates to the image boundary.

**`sharpen N`** -- Unsharp mask: `result = clamp(2 * input - blur(input, N))` per channel.

**`edge`** -- Sobel edge detection. Convert to grayscale (`gray = 0.299*R + 0.587*G + 0.114*B`),
apply Sobel X and Y kernels, compute magnitude `sqrt(Gx^2 + Gy^2)`, clamp to `[0, 255]`,
store as grayscale (set R = G = B = magnitude).

**`sepia`** -- Apply the sepia matrix:

```
R_out = clamp(0.393*R + 0.769*G + 0.189*B)
G_out = clamp(0.349*R + 0.686*G + 0.168*B)
B_out = clamp(0.272*R + 0.534*G + 0.131*B)
```

---

## Files

| File | Purpose |
|------|---------|
| `Makefile` | Must build `project1.out` with `-std=c++17` or later |
| `src/tga.hpp` | `TGAHeader`, `Pixel`, `TGAImage` declarations |
| `src/tga.cpp` | `TGAImage::read` and `TGAImage::write` implementations |
| `src/operations.hpp` | Declarations for all blend and filter functions |
| `src/operations.cpp` | Implementations of all operations |
| `src/main.cpp` | CLI entry point: argument parsing and dispatch |

You may add additional source files. Do not change the struct field layouts in `tga.hpp`.

---

## Compilation and Testing

```bash
make
./project1.out output/part1.tga input/layer1.tga multiply input/pattern1.tga
```

The grader provides the `input/` directory. For local testing, download the sample
inputs from the course portal. Create an `output/` directory before running:

```bash
mkdir -p output
```

To run the visible tests:

```bash
cd visible-tests
mkdir -p build && cd build
cmake ..
make
./tga-processor_tests
```

---

## Constraints

- Do not use `std::sort`, `std::transform`, or other STL algorithms on pixel data. Use explicit loops.
- Your Makefile must compile with `-std=c++17` or `-std=c++20`.
- The compiled binary must be named `project1.out`.
- Do not use mutable global variables.
- `sizeof(TGAHeader)` must equal 18. The grader checks this at compile time.
- `sizeof(Pixel)` must equal 3.
- Before doing anything else, `main` must verify that the host machine is
  little-endian (see Background above) and exit early if it is not. Store a
  `uint16_t` holding the value `1`, take its address, reinterpret it as an
  `unsigned char*` (the standard-permitted way to inspect the individual
  bytes of an object -- unlike a `union`, this does not have the
  type-punning caveats you saw in the union-dissector activity), and check
  whether the first byte equals `1`:

  ```cpp
  uint16_t value = 1;
  unsigned char* byte = reinterpret_cast<unsigned char*>(&value);
  bool little_endian = (byte[0] == 1);
  ```

  If `little_endian` is `false`, print exactly `error: big-endian host unsupported`
  to `std::cerr` and exit with status code `1` before parsing any command-line
  arguments or touching any file.

---

## Grading

| Component | Points |
|-----------|--------|
| Build (`make` produces `project1.out`) | 10 |
| Part 1 -- multiply | 7 |
| Part 2 -- subtract | 7 |
| Part 3 -- multiply + screen (chained) | 7 |
| Part 4 -- multiply + subtract (chained) | 7 |
| Part 5 -- overlay | 7 |
| Part 6 -- addgreen | 7 |
| Part 7 -- scalered + scaleblue | 7 |
| Part 8 -- onlyred, onlygreen, onlyblue | 7 |
| Part 9 -- combine | 7 |
| Part 10 -- flip | 7 |
| CLI error handling | 10 |
| Extended operations (parts 11-20) | 10 |
| **Total** | **100** |
| Extra credit -- `blur` | +10 |
| Extra credit -- `sharpen` | +10 |
| Extra credit -- `edge` | +10 |
| Extra credit -- `sepia` | +5 |

Parts 1-10 award partial credit based on pixel accuracy. A solution with minor
rounding differences earns most points.

The grading machine is itself little-endian, so the big-endian startup check
described in Constraints cannot be exercised by running your binary on a
big-endian host during grading, and the grader does not currently verify that
the check is present in your source. It is still a required part of the
assignment and good systems-programming practice -- write it anyway. What the
grader does verify objectively is correct little-endian decoding of `width`
and `height`: several grader input images have deliberately asymmetric,
non-round dimensions (for example 691x305) chosen so that any accidental
byte-swapping in your `read` implementation produces obviously wrong image
dimensions and fails those test cases.

---

## Submission

Submit a `.zip` file with your `Makefile` and `src/` directory at the root:

```
your-submission.zip
  Makefile
  src/
    main.cpp
    tga.hpp
    tga.cpp
    operations.hpp
    operations.cpp
```

Do not include `input/`, `output/`, or compiled binaries in your submission.

---

## Going further

- Add PNG support. PNG uses zlib compression -- compare how much more complex the
  format is compared to TGA.
- Implement Floyd-Steinberg dithering on the output of `onlyred` / `onlygreen` /
  `onlyblue`. The dithered output should look far better than naive channel zeroing.
- Add a `--help` flag that prints every operation name and formula, using ANSI color
  codes to highlight operation names.
- Profile your blur implementation with `gprof` or `perf`. A naive O(w*h*r^2)
  Gaussian can be separated into two O(w*h*r) passes -- implement it and measure
  the speedup.
