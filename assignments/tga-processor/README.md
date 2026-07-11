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

---

## Examples at a glance

To make the header layout and BGR-vs-RGB ordering completely concrete, here is
one tiny **2 pixel wide, 1 pixel tall** TGA image ("base"), shown as the exact
bytes that follow the 18-byte header:

```
byte offset (from start of pixel data): 0    1    2    3    4    5
byte value (hex):                      32   64   c8   00   fa   0a
                                        \_pixel 0 (B,G,R)_/  \_pixel 1 (B,G,R)_/
```

That is, pixel 0's three bytes on disk are `0x32, 0x64, 0xc8` and pixel 1's are
`0x00, 0xfa, 0x0a`. A second tiny image ("layer"), same dimensions, has pixel
bytes `0x64, 0x64, 0x64` and `0x80, 0x00, 0xff`. The table below shows what
every parsed value and every operation produces, checked against the actual
reference binary run on these exact files (verified with `xxd`, not guessed):

| Item | Value | Why |
|------|-------|-----|
| `header.width` | `2` | bytes `02 00` at offset 12, read as little-endian `uint16_t` -> `0x0002 = 2` |
| `header.height` | `1` | bytes `01 00` at offset 14, little-endian -> `1` |
| `header.pixelDepth` | `24` | byte `18` (hex) at offset 16 -> `0x18 = 24` decimal |
| base pixel 0, parsed | `Pixel{blue=0x32=50, green=0x64=100, red=0xc8=200}` | the FIRST byte on disk is blue, not red -- `Pixel::blue` reads the first of the three bytes |
| base pixel 1, parsed | `Pixel{blue=0, green=250, red=10}` | bytes `00 fa 0a` map to blue=0, green=0xfa=250, red=0x0a=10 |
| layer pixel 0, parsed | `Pixel{blue=100, green=100, red=100}` | bytes `64 64 64` -- a mid-gray pixel, same value in every channel |
| layer pixel 1, parsed | `Pixel{blue=128, green=0, red=255}` | bytes `80 00 ff` -- blue=0x80=128, green=0, red=0xff=255 |
| `multiply(base, layer)` pixel 0 | `red=78, green=39, blue=20` | `round(200*100/255)=78`, `round(100*100/255)=39`, `round(50*100/255)=20` |
| `multiply(base, layer)` pixel 1 | `red=10, green=0, blue=0` | `round(10*255/255)=10`; green and blue layer values are 0, so `A*0/255=0` |
| `subtract(base, layer)` pixel 0 | `red=100, green=0, blue=0` | `200-100=100`; `100-100=0`; `50-100=-50` clamps up to `0` |
| `subtract(base, layer)` pixel 1 | `red=0, green=250, blue=0` | `10-255=-245` clamps to `0`; `250-0=250`; `0-128=-128` clamps to `0` |
| `screen(base, layer)` pixel 0 | `red=222, green=161, blue=130` | `255-round((255-200)*(255-100)/255) = 255-33 = 222`, and similarly for green/blue |
| `overlay(base, layer)` pixel 0 | `red=157, green=78, blue=39` | layer's red channel is `100` (`<=127`), so the "dark blend" branch applies: `round(2*200*100/255)=157` |
| `flip` on base | pixel 0 becomes old pixel 1, pixel 1 becomes old pixel 0 | with only one row, "reverse the row order" is the same as reversing the whole pixel array |
| `onlyred` on base pixel `{200, 100, 50}` | `red=200, green=0, blue=0` | onlyred keeps the red channel and zeroes green and blue -- the pixel becomes pure red, not gray |
| `addred(base, 100)` pixel 0 | `red=255` | `200+100=300`, clamped down to `255` |
| `addred(base, -300)` pixel 0 | `red=0` | `200-300=-100`, clamped up to `0` |
| `scaleblue(base, 2.0)` pixel 0 | `blue=100` | `round(50*2.0)=100`, no clamping needed |

Because the header fields are packed with no padding between them (a 1-byte field
immediately followed by a 2-byte field), you must use `#pragma pack(1)` to tell the
compiler not to insert alignment padding. Without it, `sizeof(TGAHeader)` would be
larger than 18 and `fread` would overwrite the wrong bytes.

## Worked example: reading and multiply-blending a tiny TGA image

This traces the exact byte-by-byte path from raw file bytes to a finished
`multiply` operation, using the same `base.tga` and `layer.tga` from above.
`base.tga`'s full byte stream (18-byte header, then 6 pixel bytes) is:

```
00 00 02 00 00 00 00 00 00 00 00 00 02 00 01 00 18 00   32 64 c8 00 fa 0a
\____________________ header (18 bytes) ______________/  \_ pixel data _/
```

| Step | What happens | Result |
|------|--------------|--------|
| 1. Open file | `TGAImage::read` opens `base.tga` in binary mode with `ifstream`. | file handle ready |
| 2. Read header | `f.read(&header, sizeof(TGAHeader))` reads exactly the first 18 bytes into the packed struct. | `header.width` bytes are `02 00`, `header.height` bytes are `01 00`, `header.pixelDepth` byte is `18` |
| 3. Reassemble `width` | The two bytes `02 00` are reassembled by the (little-endian) CPU as `0x0002`. | `header.width == 2` |
| 4. Reassemble `height` | Bytes `01 00` reassemble as `0x0001`. | `header.height == 1` |
| 5. Compute pixel count | `count = width * height = 2 * 1 = 2`. | `pixels.resize(2)` |
| 6. Read pixel bytes | The next `2 * sizeof(Pixel) = 6` bytes (`32 64 c8 00 fa 0a`) are read directly into the `Pixel` array; each `Pixel` is 3 raw bytes with NO reordering at read time. | `pixels[0].blue=0x32`, `pixels[0].green=0x64`, `pixels[0].red=0xc8` |
| 7. Interpret pixel 0 | Because `Pixel`'s first byte is `blue`, the on-disk byte `0x32` becomes `blue`, `0x64` becomes `green`, `0xc8` becomes `red` -- this is the BGR-not-RGB quirk from the Background section, made concrete. | `pixels[0] = {blue=50, green=100, red=200}` |
| 8. Interpret pixel 1 | Same rule applied to bytes `00 fa 0a`. | `pixels[1] = {blue=0, green=250, red=10}` |
| 9. Read the layer image | `layer.tga` is read the same way, producing `pixels[0] = {blue=100, green=100, red=100}` and `pixels[1] = {blue=128, green=0, red=255}`. | second `TGAImage` in memory |
| 10. Apply `multiply` to pixel 0's red channel | `result = clamp(round((A * B) / 255.0))` with `A = base.pixels[0].red = 200`, `B = layer.pixels[0].red = 100`: `round(200*100/255) = round(78.43) = 78`. | `red = 78` |
| 11. Apply `multiply` to pixel 0's green and blue | Same formula per channel: green `round(100*100/255)=39`, blue `round(50*100/255)=20`. | `pixels[0] = {blue=20, green=39, red=78}` |
| 12. Repeat for pixel 1 | `A.red=10, B.red=255` -> `round(10*255/255)=10`; green and blue on the layer are `0`, so `A*0/255=0` for both. | `pixels[1] = {blue=0, green=0, red=10}` |
| 13. Write the result | `write` emits the SAME 18-byte header (unchanged, since `multiply` does not touch dimensions), then the new pixel bytes in BGR order: `14 27 4e 00 00 0a`. | output file's pixel data matches this exactly (confirmed with `xxd` against the reference binary's actual output) |

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

- **Example:** `TGAImage::read("base.tga")` on the 2x1 fixture above returns `true` and leaves `header.width == 2`, `header.height == 1`, `pixels == {{blue=50,green=100,red=200}, {blue=0,green=250,red=10}}`.
- **Error case (missing file):** `TGAImage::read("does-not-exist.tga")` returns **`false`** (the `ifstream` constructor fails to open the file, so `read` bails out immediately without touching `pixels`).
- **Error case (truncated file):** `TGAImage::read("truncated.tga")` on a file that is only 10 bytes long returns **`false`** -- the header `read` call comes up short, so the stream's fail bit is set and the function must not go on to read pixels.
- **Example (`write` after `flip`):** `img.write("out.tga")` after loading `base.tga` and running `flip` produces an 18-byte header identical to the input's, followed by the 6 pixel bytes **`00 fa 0a 32 64 c8`** (pixel order reversed, each pixel's own bytes untouched).

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

All examples below are confirmed by running the reference binary:

- **Example (no args, not an error):** `./project1.out` with no arguments prints `Project 1: Image Processing, <Season> <Year>` followed by the usage block, and **exits `0`** -- this is the one case that is NOT an error.
- **Error case (bad output extension):** `./project1.out out.png base.tga flip` -> `Invalid file name.`, exit non-zero (output does not end in `.tga`).
- **Error case (bad input extension):** `./project1.out out.tga base.png flip` -> `Invalid file name.`, exit non-zero (input does not end in `.tga`, checked the same way as output).
- **Error case (missing input file):** `./project1.out out.tga missing.tga flip` -> `File does not exist.`, exit non-zero.
- **Error case (unknown operation):** `./project1.out out.tga base.tga bogus` -> `Invalid method name.`, exit non-zero (`bogus` is not a recognized operation name).
- **Error case (missing argument):** `./project1.out out.tga base.tga addred` (no `N` given) -> `Missing argument.`, exit non-zero.
- **Error case (non-numeric argument):** `./project1.out out.tga base.tga addred abc` -> `Invalid argument, expected number.`, exit non-zero (`abc` cannot be parsed as an integer).
- **Error case (bad argument extension):** `./project1.out out.tga base.tga multiply layer.png` -> `Invalid argument, invalid file name.`, exit non-zero (the `multiply` operation's argument must itself end in `.tga`).
- **Error case (missing argument file):** `./project1.out out.tga base.tga multiply missing.tga` -> `Invalid argument, file does not exist.`, exit non-zero.

### Operations

All operations apply per-channel. Clamp all results to `[0, 255]`. Use `int` or
`float` for intermediate math to avoid overflow, then cast back to `uint8_t`.

**`multiply <file.tga>`** -- Photoshop multiply blend mode.

```
result = clamp(round((A * B) / 255.0))
```

Applied per channel (R, G, B independently).

- **Example (pixel 0):** on the fixture above, `multiply(base, layer)` pixel 0 is **`red=78, green=39, blue=20`** (`round(200*100/255)=78`, and so on per channel -- see the Worked Example section for the full derivation).
- **Tricky case (zero operand, pixel 1):** pixel 1 becomes `red=10, green=0, blue=0`: red is `round(10*255/255)=10`; green is `0` because the LAYER's green is `0` (`250*0/255=0`); blue is `0` because the BASE's blue is `0` (`0*128/255=0`) even though the layer's blue (`128`) is nonzero -- **multiplying anything by a `0` operand always yields `0`**.

**`subtract <file.tga>`** -- Subtract layer from base.

```
result = clamp(A - B, 0, 255)
```

- **Example (with clamping):** `subtract(base, layer)` pixel 1 is **`red=0, green=250, blue=0`** -- `10-255=-245` and `0-128=-128` both clamp up to `0`, while `250-0=250` needs no clamping at all.

**`screen <file.tga>`** -- Photoshop screen blend mode.

```
result = 255 - clamp(round(((255 - A) * (255 - B)) / 255.0))
```

- **Example:** `screen(base, layer)` pixel 0 is **`red=222, green=161, blue=130`** (`255 - round((255-200)*(255-100)/255) = 255 - 33 = 222`).

**`overlay <file.tga>`** -- Photoshop overlay blend mode.

Per channel, where `base` is the current image and `blend` is the layer:

```
if base <= 127:
    result = clamp(round(2 * base * blend / 255.0))
else:
    result = 255 - clamp(round(2 * (255 - base) * (255 - blend) / 255.0))
```

The branch is chosen by the LAYER's (`blend`) value, not the base image's.

- **Tricky case (else branch, pixel 1 blue):** `overlay(base, layer)` pixel 1's blue channel has `base=0, blend=128`; since **`blend > 127`** it takes the "else" branch: `255 - round(2*(255-0)*(255-128)/255) = 255 - 254 = 1`.
- **Example (if branch, pixel 0 red):** pixel 0's red channel has `base=200, blend=100`; since **`blend <= 127`** it takes the "if" branch: `round(2*200*100/255) = 157`.

**`combine <r.tga> <g.tga> <b.tga>`** -- Merge three channel images. Take the red
channel from `r.tga`, green from `g.tga`, blue from `b.tga`.

- **Example:** using a third fixture `rsrc.tga` (pixel 0 = `{red=77, green=9, blue=9}`) as the red source, `base.tga` as the green source, and `layer.tga` as the blue source, `combine` pixel 0 comes out as **`{red=77 (from rsrc), green=100 (from base), blue=100 (from layer)}`** -- confirmed against the reference binary's actual output bytes (`64 64 4d`).
- **Tricky case (discarded channels):** `rsrc`'s own green (`9`) and blue (`9`) values are **discarded entirely**; only its red channel is used.

**`flip`** -- Vertical flip. Reverse the row order.

- **Example:** on a 2x1 image (one row), `flip` reverses the whole pixel array, turning `{blue=50,green=100,red=200}, {blue=0,green=250,red=10}` into **`{blue=0,green=250,red=10}, {blue=50,green=100,red=200}`** -- confirmed against the reference binary's actual output bytes (`00 fa 0a 32 64 c8`).
- **Tricky case (taller image):** rows are reversed as whole units -- pixels within a row keep their left-to-right order; only which row comes first changes.

**`onlyred`** -- Set G = 0, B = 0 for every pixel.
**`onlygreen`** -- Set R = 0, B = 0 for every pixel.
**`onlyblue`** -- Set R = 0, G = 0 for every pixel.

- **Example:** `onlyred` on a pixel `{red=200, green=100, blue=50}` produces **`{red=200, green=0, blue=0}`** -- only the red channel survives, the other two are zeroed out (not replaced with red's value, so the result is a **pure red pixel, not a gray one**).

**`addred N`**, **`addgreen N`**, **`addblue N`** -- Add integer `N` to one channel.
`N` may be negative. Clamp the result.

- **Example:** `addred(base, 100)` on pixel 0 (`red=200`) gives **`red=255`** (`200+100=300` clamps down to `255`).
- **Tricky case (clamp low):** `addred(base, -300)` on the same pixel gives **`red=0`** (`200-300=-100` clamps up to `0`).

**`scalered N`**, **`scalegreen N`**, **`scaleblue N`** -- Multiply one channel by
float `N`. Clamp the result.

- **Example:** `scaleblue(base, 2.0)` on pixel 0 (`blue=50`) gives **`blue=100`** (`round(50*2.0)=100`, no clamping needed).
- **Tricky case (clamp high):** `scalered(base, 5.0)` on the same pixel (`red=200`) gives **`red=255`** (`round(200*5.0)=1000` clamps down to `255`).

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
