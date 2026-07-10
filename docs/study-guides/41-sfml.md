# Study Guide 41: SFML

This module introduces SFML (Simple and Fast Multimedia Library), a C++
library -- not a language feature, just a set of classes you `#include`
and call -- for opening a window, drawing 2D graphics, and reacting to
input. sfml-anatomy builds the mental model (the game loop, the event
queue, the coordinate system, and SFML's core object family) entirely by
reading and reasoning about code fragments, no compiling required.
sfml-canvas then has students implement five pixel-drawing routines
against `sf::Image` alone -- SFML's CPU-only, no-window, no-GPU pixel
buffer type -- so the work can be graded automatically without a display.

## Know before you start

- What a library is: already-compiled code a program `#include`s and
  links against rather than writing itself [assumed: row 40 -- Libraries
  (static vs. dynamic)]
- Function declarations, structs, and basic class/object syntax (SFML's
  API is entirely classes and methods) [assumed: row 6 -- Control &
  Functions; row 21 -- OOP Implementation in C++]

## Taught here

Concept: the game loop
- Know that an SFML program is built around a `while (window.isOpen())`
  loop that repeats once per frame (frame: one pass through the loop --
  clear the window, draw everything, show it -- repeated dozens of times
  per second to create the illusion of smooth motion).
- Know the four-beat skeleton of a frame: drain events, `clear()` (wipe
  the back buffer -- the off-screen image SFML draws into; nothing drawn
  is visible until this finished image is swapped onto the screen),
  `draw()` (paint shapes/sprites into that buffer, any number of times),
  `display()` (swap the finished back buffer onto the actual screen).
- Know that skipping `clear()` while still drawing and displaying does
  not blank the screen or crash the program -- it leaves every previous
  frame's drawing on screen, since nothing ever erases the old pixels, so
  a moving shape leaves a smeared trail of every past position.
- Know that skipping `display()` means `clear()` and `draw()` still ran
  and did real work, but none of it ever reached the screen -- the window
  keeps showing whatever was already there.
- Know the game loop itself is a cooperative EVENT LOOP, here implemented
  on a single thread (typical for this kind of loop, though not required
  by the event-loop concept itself) -- not threading, and not a hardware
  interrupt handler directly (the OS absorbs the real interrupt and
  delivers it as a queued item `pollEvent` reads); see row 55's
  `who-handles-the-wait` for the full disambiguation.

Concept: the event queue
- Know that an event is something that happened since the last check (a
  key press, a mouse move, the window's close button being clicked), and
  SFML collects these into an internal queue (a first-in-first-out list)
  as they occur rather than interrupting the program's code the instant
  they happen.
- Know that `pollEvent(event)` pops exactly one event off that queue per
  call and returns whether one was available; calling it inside a `while`
  loop drains the entire queue every frame, while calling it inside an
  `if` would process only the first queued event and silently leave the
  rest queued and increasingly stale -- several events (fast typing,
  mouse movement) can queue up within a single frame.
- Know `sf::Event::Closed` fires once when the user requests the window
  be closed at the OS/window-manager level (the X button, Alt+F4); it
  does not close the window itself -- the program must call
  `window.close()` in response, or the window keeps running.
- Know `sf::Event::KeyPressed` is a separate, unrelated event type firing
  once per keyboard key going down.

Concept: SFML's coordinate system
- Know SFML places its coordinate origin `(0, 0)` at the window's
  top-left corner, with x growing rightward and y growing DOWNWARD --
  the opposite of the math-class (Cartesian) convention where y grows
  upward, but the same convention most 2D graphics and GUI systems use.
- Be able to reason about `setPosition(x, y)`: a smaller y places a shape
  nearer the top of the window; a y value close to the window's height
  places it near the bottom.

Concept: SFML's core object family
- Know `sf::Vector2f` is a plain struct-like pair of public float fields
  `x` and `y` (also `sf::Vector2i` for ints, `sf::Vector2u` for unsigned),
  used throughout SFML for positions, sizes, and velocities -- ordinary
  field access and arithmetic apply directly (`velocity.y += 5.f`).
- Know shapes (`sf::CircleShape`, `sf::RectangleShape`, ...) expose
  setter methods that configure appearance and placement before drawing:
  `setPosition()` for location, `setFillColor()` for interior color,
  `setOutlineColor()`/`setOutlineThickness()` for the border; a
  constructor argument like `sf::CircleShape(25.f)` sets a shape property
  (here, radius), not its color -- shapes default to white fill until
  `setFillColor()` is called.
- Know `window.draw()` paints an object using whatever properties are
  already set on it; it takes no color argument itself, which is exactly
  why setters must run before `draw()`.
- Know `sf::Color` stores four channels -- red, green, blue, alpha
  (opacity: 0 fully transparent, 255 fully opaque) -- each as an 8-bit
  unsigned value from 0 to 255 (the same representation as classic
  RGB(A) values in most image formats and web CSS colors), not a 0-to-1
  normalized float as some other graphics APIs use.
- Know the texture/sprite split: `sf::Texture` is the heavyweight
  resource -- `loadFromFile()` decodes an image file and uploads its
  pixel data to the GPU, real and relatively expensive work, done once
  per unique image. `sf::Sprite` is a lightweight, cheap-to-create
  drawable that references a texture via `setTexture()` (which does not
  copy pixel data) plus its own position/rotation/scale -- many sprites
  can cheaply share one loaded texture.
- Know draw order is SFML's only depth rule (the "painter's algorithm,"
  named for a painter laying down background first, then closer objects
  on top): SFML has no automatic z-ordering, so it paints strictly in the
  order `draw()` is called, each call painting directly over whatever is
  already in the back buffer where shapes overlap -- the last thing
  drawn ends up visibly on top.

Concept: frame-rate independence
- Know that moving an object by a fixed number of pixels per frame (with
  no time factor) is a bug on real hardware, because frame rate varies by
  machine: a 144 FPS machine runs the loop body roughly 2.4x as often per
  real second as a 60 FPS machine, so the same "move 2 pixels per frame"
  code produces roughly 2.4x the on-screen speed -- a fixed per-frame
  amount is really a per-frame speed, and frames do not take a fixed
  amount of real time.
- Know the fix is delta time (dt): elapsed real time since the last
  frame, typically measured in seconds with `sf::Clock::restart()`, used
  to scale movement (`shape.move(speed * dt, 0.f)`) so an object covers
  the same real-world distance per second regardless of frame rate.

Concept: sf::Image as a headless, CPU-only pixel buffer
- Know `sf::Image` is a 2D grid of `sf::Color` pixels living entirely in
  the program's own memory -- no window, no GPU, nothing rendered to a
  screen -- distinct from `sf::RenderWindow` (an actual on-screen window)
  and `sf::RenderTexture` (a GPU render target).
- Know `sf::Image` uses the same top-left-origin, y-grows-down coordinate
  convention as the windowed API; pixels are read with `img.getPixel(x,
  y)` and written with `img.setPixel(x, y, color)`, and an image can be
  written to disk with `img.saveToFile(...)`.
- Know why this matters for automated grading: an automated grading
  server almost never has a real display attached, so any code that
  opens an actual window (`sf::RenderWindow`) or renders to the GPU
  (`sf::RenderTexture`) cannot be graded automatically there.
  `sf::Image`-only code touches neither, so it runs identically -- and
  produces the exact same pixels -- on a laptop and on a headless grading
  server.

Concept: pixel-level drawing routines (sfml-canvas)
- Be able to compute a per-channel linear interpolation ("lerp") between
  two `sf::Color` values across a gradient's width, applied identically
  down every row/column.
- Be able to tile an image into fixed-size blocks and alternate between
  two colors by the parity (even/odd) of the sum of a block's two
  integer-divided indices.
- Be able to translate a mathematical shape (a circle of radius r
  centered at `(cx, cy)`) into a pixel-by-pixel membership test evaluated
  over a bounding region: `(px - cx)^2 + (py - cy)^2 <= r^2`, the actual
  distance test rather than a bounding-square approximation.
- Be able to clip a drawing operation so it never writes to a pixel
  outside an image's bounds (`[0, width) x [0, height)`), instead of
  resizing the image or crashing on an out-of-range coordinate.
- Be able to alpha-blend two same-size images per pixel and per channel
  as a weighted average: `result = base * (1 - alpha) + overlay * alpha`,
  where alpha 0 reproduces `base` exactly and alpha 1 reproduces
  `overlay` exactly.
- Know the round-half-up rule used for every fractional channel value
  produced by these computations (`static_cast<sf::Uint8>(value + 0.5f)`)
  and why it must be applied consistently: a different rounding rule
  (round-to-even, truncation) can disagree with round-half-up exactly at
  values halfway between two integers, and an exact-pixel-match grader
  has no tolerance for that disagreement.
- Be able to draw a 1-pixel-wide rectangle outline (top row, bottom row,
  left column, right column only, no filled interior) with the same
  edge-clipping discipline as the disk routine.

## Study checklist

- [ ] Recite the four-beat frame skeleton and explain what visibly
      breaks if `clear()` or `display()` is skipped.
- [ ] Explain why `pollEvent` belongs in a `while` loop, not an `if`.
- [ ] Given an `sf::Event::Closed` handler, explain why it does not
      close the window by itself.
- [ ] Given two `setPosition(x, y)` calls, say which places a shape
      lower on screen and why.
- [ ] Explain the cost difference between `sf::Texture` and `sf::Sprite`
      and why one texture can back many sprites.
- [ ] State `sf::Color`'s four channels and their numeric range.
- [ ] Predict which of several overlapping `draw()` calls ends up on top.
- [ ] Explain why a fixed per-frame movement amount is frame-rate
      dependent, and how dt fixes it.
- [ ] Explain why `sf::Image`-only code can be graded on a headless
      server while `sf::RenderWindow` code cannot.
- [ ] Write the circle membership test and the row-major checkerboard
      parity rule from memory.
- [ ] State the round-half-up rounding rule and why an exact-pixel-match
      grader requires it consistently.

## Practiced in

`sfml-anatomy`, `sfml-canvas`
