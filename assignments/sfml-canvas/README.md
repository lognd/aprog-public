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

## Task

Implement these five functions in `canvas.cpp`, against the fixed
declarations in `canvas.hpp` (do not modify `canvas.hpp`):

### `make_gradient(width, height, from, to)`

Build a `width x height` image where column `x`'s color is a linear
interpolation between `from` (at `x = 0`) and `to` (at `x = width - 1`),
computed independently for each of the four channels (r, g, b, a). Every
row is identical -- the whole image is a horizontal gradient repeated down
every column. If `width <= 1`, every pixel is `from`.

### `checkerboard(width, height, cell, a, b)`

Tile the image into `cell x cell` pixel blocks, alternating between colors
`a` and `b`. The pixel at `(x, y)` belongs to block `(x / cell, y / cell)`
(integer division); if the sum of those two block indices is even, use
color `a`, otherwise `b`. Block `(0, 0)` -- the block containing the
top-left pixel -- is always `a`.

### `draw_disk(img, cx, cy, r, color)`

Paint a filled circle of radius `r` centered at pixel `(cx, cy)` directly
onto `img` (which is not resized). A pixel `(px, py)` is part of the disk
exactly when `(px - cx)^2 + (py - cy)^2 <= r^2` -- the distance test, not
a bounding square. Any part of the disk that would fall outside `img`'s
bounds is simply skipped (clipped); never write outside
`[0, img.getSize().x) x [0, img.getSize().y)`.

### `blend(base, overlay, alpha)`

Combine two same-size images into a new one, per pixel and per channel:

```
result_channel = base_channel * (1 - alpha) + overlay_channel * alpha
```

`alpha = 0` reproduces `base` exactly; `alpha = 1` reproduces `overlay`
exactly. `base` and `overlay` are always the same size in every graded
case; the image you return must have that same size.

### `outline_rect(img, x, y, w, h, color)`

Draw a 1-pixel-wide border directly onto `img`, tracing the rectangle
whose pixels span `[x, x + w)` horizontally and `[y, y + h)` vertically:
its top row, bottom row, left column, and right column. Do not fill the
interior. Clip any border pixel that would fall outside `img`'s bounds.

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
