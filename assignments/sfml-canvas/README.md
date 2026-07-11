# SFML Canvas

SFML (Simple and Fast Multimedia Library) is the graphics library your
course project will use to open a window and draw to the screen. Before
you get there, this assignment has you work with the piece of SFML that
has nothing to do with windows at all: `sf::Image`, a plain grid of pixels
that lives entirely in your program's own memory. You will write five
small functions that build and edit images pixel by pixel -- a gradient, a
checkerboard, a filled circle, an alpha-blended combination of two images,
and a rectangle outline -- and save your results as PNG files you can open
and look at.

## Learning goals

- Work with `sf::Image` and `sf::Color` as plain, CPU-only pixel data --
  no window, no GPU, nothing rendered to a screen
- Compute per-channel linear interpolation (a "lerp") between two colors
- Translate a mathematical shape (a circle) into a pixel-by-pixel test
  (`dx*dx + dy*dy <= r*r`) evaluated over a bounding region
- Clip a drawing operation so it never writes outside an image's bounds
- Combine two images with alpha blending (a weighted average per channel)
- Apply a single rounding rule consistently across every function that
  produces a fractional pixel value

## Background

An `sf::Image` is a 2D grid of `sf::Color` values -- one color per pixel,
each stored as four 8-bit numbers: red, green, blue, and alpha (opacity),
every value from 0 to 255. You size one with `img.resize({width,
height}, color)` (or build it directly, `sf::Image img({width, height},
color)`), read any pixel with `img.getPixel({x, y})`, and write any
pixel with `img.setPixel({x, y}, color)` -- in SFML 3 a pixel
coordinate is a single `sf::Vector2u`, hence the `{x, y}` braces.
Coordinates use SFML's usual convention: `(0, 0)` is the top-left
corner, `x` grows right, `y` grows **down**.

> **SFML version:** this assignment is graded against **SFML 3**, so use
> the SFML 3 spellings above. If you only have the older SFML 2.x
> installed, the equivalent calls are `img.create(width, height,
> color)`, `img.getPixel(x, y)`, and `img.setPixel(x, y, color)` (two
> separate integer arguments, and `sf::Uint8` in place of
> `std::uint8_t`) -- you can develop against 2.x, but the version you
> submit against is 3. See the [Install SFML
> activity](../../activities/env-setup-sfml/) for getting SFML 3.

This is a different object from `sf::RenderWindow` (which opens an actual
window on screen) and `sf::RenderTexture` (which renders to a GPU
texture). `sf::Image` touches neither a display nor a GPU -- it is just
memory you can read, write, and save to a file with
`img.saveToFile("out.png")`. That matters for grading: an automated
grading server almost never has a real display attached (there is no
monitor, no window manager, nothing to click on), so any assignment that
opens a window cannot be graded automatically there. Every function in
this assignment works with `sf::Image` alone, which means it runs the same
way -- and produces the exact same pixels -- on your laptop and on the
grading server. `sfml-anatomy`, a separate ungraded activity, covers the
windowed game loop (`sf::RenderWindow`, the event queue, `clear`/`draw`/
`display`) that your actual course project will use; that material is not
tested here, precisely because it cannot be graded headlessly.

## Examples at a glance

To make all five functions concrete before you write any code, here is
**one** running example: a `4x4` canvas. Read this section first -- it is
the whole assignment in miniature. Colors are written as `(r, g, b, a)`,
each channel `0` to `255`.

`make_gradient(4, 4, from=(0,0,0,255), to=(30,60,90,255))` builds this image
(every row is identical, so only one row is shown):

```
 column:   x=0            x=1             x=2             x=3
 color :  (0,0,0,255)  (10,20,30,255)  (20,40,60,255)  (30,60,90,255)
```

`checkerboard(4, 4, 2, a=black(0,0,0,255), b=white(255,255,255,255))` builds
this image (`A` = black, `B` = white):

```
 A A B B
 A A B B
 B B A A
 B B A A
```

| Call | Result | Why |
|------|--------|-----|
| `make_gradient(4, 4, black, (30,60,90,255))` | grid above | column `x`'s color is `black` lerped toward `(30,60,90,255)` by `t = x / (width - 1)`; every row repeats it |
| `make_gradient(1, 3, (10,20,30,255), (200,200,200,255))` | every one of the 3 pixels is `(10,20,30,255)` | `width <= 1` means there is no second column to lerp toward, so every pixel is `from` |
| `checkerboard(4, 4, 2, black, white)` | grid above | block `(x/2, y/2)`; block `(0,0)` (top-left) is always `a` = black; even block-index sums stay black, odd sums flip to white |
| `checkerboard(5, 5, 10, black, white)` | every pixel is black | `cell = 10` is bigger than the whole `5x5` image, so every pixel falls in block `(0,0)` -- no tiling is visible at all |
| `draw_disk(img, 2, 2, 1, red)` on a 4x4 white canvas | paints `(2,1) (1,2) (2,2) (3,2) (2,3)` -- a plus/cross shape | each candidate pixel `(px,py)` is painted only if `(px-2)^2+(py-2)^2 <= 1^2`; see the worked example below |
| `draw_disk(img, 5, 5, 0, red)` | paints only the single pixel `(5,5)` | with `r = 0`, only `dx = dy = 0` satisfies `dx*dx+dy*dy <= 0` |
| `blend(gradient, checkerboard, 0.5)` at pixel `(2, 0)` | `(138,148,158,255)` | base `(20,40,60,255)` and overlay-white `(255,255,255,255)` average per channel, e.g. `r = 20*0.5 + 255*0.5 = 137.5`, which round-half-up turns into `138` |
| `blend(base, overlay, 0.f)` (any images) | exactly `base`, pixel for pixel | `alpha = 0` means the overlay term is multiplied by `0` and drops out entirely |
| `outline_rect(img, 1, 1, 3, 3, black)` on a 6x6 white canvas | paints the 8-pixel ring around `(2,2)`, leaves `(2,2)` white | the border traces the rectangle's 4 edges; `(2,2)` is the one interior pixel, never touched |
| `outline_rect(img, 1, 1, 2, 2, black)` on a 4x4 canvas | paints all 4 pixels of the 2x2 block, no white pixel left inside | a `2x2` rectangle's border already covers every one of its pixels -- there is no interior left over |
| `outline_rect(img, -2, -2, 7, 7, black)` on a 5x5 canvas | paints the entire bottom row (`y=4`) and the entire right column (`x=4`); the rest of the border (top row `y=-2`, left column `x=-2`) is clipped away | only the part of the rectangle's border that still lands inside `[0,5) x [0,5)` gets drawn; the rest is silently skipped, never a crash |

## Worked example: watch `draw_disk` paint pixel by pixel, step by step

This is the single most important thing to understand about `draw_disk`, so
here is every candidate pixel checked, one at a time. We call
`draw_disk(img, 2, 2, 1, red)` on a `4x4` all-white canvas: center
`(cx, cy) = (2, 2)`, radius `r = 1`.

The function loops `dy` from `-r` to `r`, and for each `dy`, loops `dx` from
`-r` to `r` -- checking every pixel in the bounding square first, then using
the distance test `dx*dx + dy*dy <= r*r` to decide whether that pixel is
really inside the circle (not just the square). `r*r` here is `1`.

| Step | `dx` | `dy` | `dx*dx+dy*dy` | Compare to `r*r = 1` | Pixel `(cx+dx, cy+dy)` | In bounds `[0,4)x[0,4)`? | Action |
|------|------|------|---------------|-----------------------|------------------------|--------------------------|--------|
| 1 | -1 | -1 | 2 | `2 > 1` | (1,1) | yes | skip -- outside the circle |
| 2 | 0  | -1 | 1 | `1 <= 1` | (2,1) | yes | paint red |
| 3 | 1  | -1 | 2 | `2 > 1` | (3,1) | yes | skip -- outside the circle |
| 4 | -1 | 0  | 1 | `1 <= 1` | (1,2) | yes | paint red |
| 5 | 0  | 0  | 0 | `0 <= 1` | (2,2) | yes | paint red (the center is always inside) |
| 6 | 1  | 0  | 1 | `1 <= 1` | (3,2) | yes | paint red |
| 7 | -1 | 1  | 2 | `2 > 1` | (1,3) | yes | skip -- outside the circle |
| 8 | 0  | 1  | 1 | `1 <= 1` | (2,3) | yes | paint red |
| 9 | 1  | 1  | 2 | `2 > 1` | (3,3) | yes | skip -- outside the circle |

Every one of the 9 candidate pixels in the bounding square was in bounds
here, so none were clipped in this example -- but the same in-bounds check
(`px < 0 || py < 0 || px >= w || py >= h`) runs on every step regardless,
which is what protects a disk near an edge from ever writing outside the
image.

The final `4x4` grid, `.` for untouched white and `X` for painted red:

```
 . . . .
 . . X .
 . X X X
 . . X .
```

That is a plus/cross shape, not a diamond or a square -- notice steps 1, 3,
7, and 9 (the four diagonal corners of the bounding square) were all
skipped, because a corner of a square is always farther from the center
than the square's own edge midpoints, and the distance test rejects
anything farther than `r`.

## Task

Implement these five functions in `canvas.cpp`, against the fixed
declarations in `canvas.hpp` (do not modify `canvas.hpp`):

### `make_gradient(width, height, from, to)`

Build a `width x height` image where column `x`'s color is a linear
interpolation between `from` (at `x = 0`) and `to` (at `x = width - 1`),
computed independently for each of the four channels (r, g, b, a). Every
row is identical -- the whole image is a horizontal gradient repeated down
every column. If `width <= 1`, every pixel is `from`.

- **Example (basic gradient):** `make_gradient(4, 4, (0,0,0,255),
  (30,60,90,255))` gives columns `x=0 -> (0,0,0,255)`, `x=1 ->
  (10,20,30,255)`, `x=2 -> (20,40,60,255)`, **`x=3 -> (30,60,90,255)`**,
  the same down every row.
- **Edge case (width <= 1):** `make_gradient(1, 3, (10,20,30,255),
  (200,200,200,255))` -- all 3 pixels are exactly **`(10,20,30,255)`**;
  `to` is never reached because there is no second column to lerp toward.
- **Rounding edge case:** `make_gradient(3, 1, (0,0,0,255),
  (9,10,11,255))` at `x=1` (`t = 0.5` exactly) gives **`(5,5,6,255)`** --
  `4.5` rounds up to `5`, `5.0` stays `5`, `5.5` rounds up to `6`
  (round-half-up, per the rule below).

### `checkerboard(width, height, cell, a, b)`

Tile the image into `cell x cell` pixel blocks, alternating between colors
`a` and `b`. The pixel at `(x, y)` belongs to block `(x / cell, y / cell)`
(integer division); if the sum of those two block indices is even, use
color `a`, otherwise `b`. Block `(0, 0)` -- the block containing the
top-left pixel -- is always `a`.

- **Example (basic tiling):** `checkerboard(4, 4, 2, black, white)` gives
  the `4x4` grid `A A B B / A A B B / B B A A / B B A A` (`A` = black,
  `B` = white) -- see the "Examples at a glance" section above for the
  full picture.
- **Edge case (1x1 image):** `checkerboard(1, 1, 2, black, white)` -- the
  one pixel is block `(0/2, 0/2) = (0, 0)`, sum `0` is even, so the pixel
  is **`black`**.
- **Edge case (cell bigger than the image):** `checkerboard(5, 5, 10,
  black, white)` -- every pixel falls in block `(0, 0)`, so the entire
  `5x5` image is **a single solid color, `black`**, with no visible
  tiling at all.

### `draw_disk(img, cx, cy, r, color)`

Paint a filled circle of radius `r` centered at pixel `(cx, cy)` directly
onto `img` (which is not resized). A pixel `(px, py)` is part of the disk
exactly when `(px - cx)^2 + (py - cy)^2 <= r^2` -- the distance test, not
a bounding square. Any part of the disk that would fall outside `img`'s
bounds is simply skipped (clipped); never write outside
`[0, img.getSize().x) x [0, img.getSize().y)`.

- **Example (basic disk):** on a `4x4` white canvas, `draw_disk(img, 2,
  2, 1, red)` paints exactly the plus-shaped **5 pixels** `(2,1) (1,2)
  (2,2) (3,2) (2,3)` -- worked out step by step in the "Worked example"
  section above.
- **Edge case (r = 0):** `draw_disk(img, 5, 5, 0, red)` paints only the
  **single center pixel `(5,5)`** -- the distance test `0*0+0*0 <= 0*0`
  is true only for `dx = dy = 0`.
- **Edge case (fully off-image):** `draw_disk(img, -100, -100, 3, red)`
  on any image leaves **every pixel untouched** and does not crash or
  resize the image -- every candidate pixel in the bounding square clips
  away.

### `blend(base, overlay, alpha)`

Combine two same-size images into a new one, per pixel and per channel:

```
result_channel = base_channel * (1 - alpha) + overlay_channel * alpha
```

`alpha = 0` reproduces `base` exactly; `alpha = 1` reproduces `overlay`
exactly. `base` and `overlay` are always the same size in every graded
case; the image you return must have that same size.

- **Example (basic blend):** blending the gradient and checkerboard
  images from "Examples at a glance" at `alpha = 0.5`, pixel `(2, 0)`:
  base `(20,40,60,255)`, overlay white `(255,255,255,255)` ->
  **`(138,148,158,255)`** (channel r: `20*0.5 + 255*0.5 = 137.5`, which
  round-half-up turns into `138`).
- **Edge case (alpha = 0):** `blend(base, overlay, 0.f)` reproduces
  **`base` exactly**, pixel for pixel, for any two same-size images.
- **Edge case (1x1 images):** `blend` on two `1x1` images, `base =
  (0,0,0,255)` and `overlay = (9,10,11,255)`, at `alpha = 0.5` gives
  **`(5,5,6,255)`** -- the same rounding rule as `make_gradient`'s
  midpoint example, because the math is identical.

### `outline_rect(img, x, y, w, h, color)`

Draw a 1-pixel-wide border directly onto `img`, tracing the rectangle
whose pixels span `[x, x + w)` horizontally and `[y, y + h)` vertically:
its top row, bottom row, left column, and right column. Do not fill the
interior. Clip any border pixel that would fall outside `img`'s bounds.

- **Example (basic ring):** on a `6x6` white canvas, `outline_rect(img,
  1, 1, 3, 3, black)` paints the 8-pixel ring around `(2, 2)` -- `(1,1)
  (2,1) (3,1) (1,2) (3,2) (1,3) (2,3) (3,3)` -- and leaves **`(2, 2)`**
  (the one interior pixel) white.
- **Edge case (rect too small to have an interior):** `outline_rect(img,
  1, 1, 2, 2, black)` on a `4x4` canvas paints **all 4 pixels** of the
  2x2 block -- a 2x2 rectangle's own border already covers every pixel
  it has, leaving no interior pixel behind.
- **Edge case (clipping):** `outline_rect(img, -2, -2, 7, 7, black)` on a
  `5x5` canvas paints the entire bottom row (`y = 4`) and the entire
  right column (`x = 4`) -- the parts of the border still inside `[0,5)
  x [0,5)` -- while the top row (`y = -2`) and left column (`x = -2`)
  are **clipped away entirely**, with no crash.

### Rounding rule (applies to `make_gradient` and `blend`)

Both functions compute a fractional channel value (a float) and must
round it to an integer 0-255 for storage in `sf::Color`. Use round-half-up:

```cpp
std::uint8_t channel = static_cast<std::uint8_t>(value + 0.5f);
```

where `value` is the exact computed float, before rounding. This matters
for grading: a different rounding rule (round-to-even, truncation) can
disagree with round-half-up on values exactly halfway between two
integers, and the grader checks for an exact pixel match.

## Files

| File | Purpose |
|------|---------|
| `canvas.hpp` | Fixed function declarations -- do not modify |
| `canvas.cpp` | Implement all five functions here |
| `visible-tests/test_catch.cpp` | Visible Catch2 tests you can run locally |

## Compilation and Testing

```bash
mkdir build && cd build
cmake ../visible-tests -DSUBMISSION_DIR=<path-to-your-submission>
cmake --build .
./sfml-canvas_tests
```

`SUBMISSION_DIR` tells CMake where to find your `canvas.hpp` and
`canvas.cpp`. This requires **SFML 3** installed locally (note that
Debian/Ubuntu's `apt` package `libsfml-dev` still installs SFML 2.5.1 --
see the [Install SFML activity](../../activities/env-setup-sfml/) for
building SFML 3); the grading server provides SFML 3 automatically, so
you do not need to configure anything for submission.

## Constraints

- Do not modify `canvas.hpp`.
- Do not use `sf::RenderWindow` or `sf::RenderTexture` anywhere in
  `canvas.cpp` -- every function must work with `sf::Image` alone, so the
  assignment can be graded without a display.
- Round every fractional channel value with round-half-up, exactly as
  specified above -- the grader checks for an exact pixel match against a
  reference image, not an approximate one.
- `draw_disk` must use the distance test `dx*dx + dy*dy <= r*r`, not a
  bounding square or any other approximation of a circle.
- Every drawing function (`draw_disk`, `outline_rect`) must clip cleanly
  at the image's edges -- never write to a pixel outside the image, and
  never resize or crash on out-of-bounds coordinates.

## Grading

| Component | Points |
|-----------|--------|
| Compilation | 0 (required to proceed) |
| No `sf::RenderWindow`/`sf::RenderTexture` (source check) | 10 |
| Visible tests (Catch2) | 30 |
| Hidden tests (Catch2, exact pixel match against reference images) | 60 |
| **Total** | **100** |

## Submission

Submit a single file named `canvas.cpp`. Do not rename it, and do not
submit `canvas.hpp` -- the grader uses its own fixed copy.

## Going further

- Once your five functions pass, install SFML locally and write a tiny
  `sf::RenderWindow` program (see the `sfml-anatomy` activity) that loads
  one of your saved PNGs with `sf::Texture::loadFromFile` and displays it
  in a real window with an `sf::Sprite`.
- Add a sixth function, `draw_ring(img, cx, cy, r_inner, r_outer, color)`,
  that paints an annulus (a ring) using two distance tests instead of one.
- `blend` currently requires `base` and `overlay` to already be the same
  size. Rewrite it (on a scratch copy) to blend only the overlapping
  region when they differ in size, and think through what should happen
  to the rest of the returned image.
- Try grading your own code with SFML uninstalled (temporarily rename
  `/usr/include/SFML`, or use a container without it) and read the
  compiler error `find_package(SFML ...)` produces -- this is exactly the
  error the grading server would produce if `libsfml-dev` were missing
  from its dependency list.
