# Activity: SFML Anatomy

SFML (Simple and Fast Multimedia Library) is a C++ library for opening a
window, drawing 2D graphics into it, and reacting to keyboard and mouse
input. It is not a language feature -- it is a set of classes you `#include`
and call, the same as any other library. This activity walks through the
handful of ideas every SFML program is built from before you touch your
course project's real code: the game loop (the `while` loop every frame
runs through), the event queue (how SFML tells you about key presses and
window-close clicks), the coordinate system (where pixel `(0, 0)` actually
is), and the small family of objects -- `sf::Vector2f`, shapes, textures,
sprites, `sf::Color` -- that almost every SFML program touches.

## Background

Every question below shows a short, real SFML code fragment and asks you
to reason about what it does. You do not need SFML installed to do this
activity -- you are reading and reasoning about code, not compiling it.
(If you do have SFML installed, you are welcome to try the fragments
yourself; `sfml-canvas`, a separate graded assignment, is where you will
actually write and compile SFML code.)

A few terms used throughout:

- **Window**: the on-screen area your program draws into, represented in
  SFML by an `sf::RenderWindow`.
- **Frame**: one pass through the main loop -- clear the window, draw
  everything, show it. A game or graphical program repeats this dozens of
  times per second to create the illusion of smooth motion.
- **Event**: something that happened since the last time you checked --a
  key was pressed, the mouse moved, the user clicked the close button.
  SFML collects these into a queue (a first-in-first-out list) rather than
  interrupting your code the instant they happen.
- **Back buffer**: the off-screen image SFML draws into. Nothing you draw
  is visible until that finished image is swapped onto the screen.

The `while (window.isOpen())` game loop is, precisely, a cooperative
**event loop** -- the same kind of machine `asyncio`'s event loop is,
just written by hand instead of provided by a library, and (as is
typical for this kind of loop, though not required by the event-loop
concept itself) implemented here on a single thread. One worker (your
program's one thread) repeatedly asks "what happened since I last
checked?" via `pollEvent()`, and nothing about that loop uses threading
(there is no second worker the OS is switching to) or a hardware
interrupt directly (your code never receives a raw interrupt; the
operating system absorbs the real hardware signal -- a key going down,
a mouse moving -- and hands your loop an already-packaged event to find
in the queue whenever `pollEvent()` next checks). If the difference
between an event loop and threading is fuzzy, `who-handles-the-wait`
(row 55) is the dedicated activity that untangles event loops,
threading, and concurrency vs. parallelism side by side -- with this
exact loop as one of its comparison points, and hardware interrupts
covered there as extra depth.

## Concepts covered

- The game loop skeleton: `isOpen` / `pollEvent` / `clear` / `draw` / `display`
- Why `pollEvent` is called in a `while` loop, not an `if`
- SFML event types (`sf::Event::Closed`, `sf::Event::KeyPressed`, ...)
- SFML's coordinate system: origin at the top-left, `y` growing downward
- `sf::Vector2f` as a plain `{x, y}` pair used for positions and velocities
- Shape setters (`setPosition`, `setFillColor`) vs. `window.draw`
- Frame-rate independence: why movement should multiply by elapsed time (`dt`)
- The texture/sprite split: one heavyweight resource, many lightweight drawables
- `sf::Color`'s four 0-255 channels (red, green, blue, alpha)
- Draw order as SFML's only depth rule (the "painter's algorithm")

## How it works

Twelve questions, each showing a short SFML code fragment. Some ask what
a fragment prints or does; some ask you to fill in a missing call; some
ask you to explain *why* a fragment behaves the way it does. Type your
answer exactly as instructed in the prompt (a single word, a short phrase,
or one of a small set of listed choices). Wrong answers show an
explanation of why that answer is wrong and let you try again immediately.
The passphrase is revealed once every question is answered correctly.

## Getting started

```bash
python3 launch.py
```

## You will know you are done when...

All twelve questions are answered correctly and the program prints the
passphrase.

## Going further

- Install SFML (`libsfml-dev` on Debian/Ubuntu) and write a five-line
  program that opens a window, draws one circle, and runs the game loop
  from question 1. Watch it actually appear.
- Comment out `window.clear()` in your own test program (not just read
  about it) and watch the smear effect from question 2 happen live.
- Once you have SFML installed, work through `sfml-canvas` -- a graded
  assignment that has you manipulate pixels directly with `sf::Image`,
  no window required, so it can be graded automatically. It uses the same
  `sf::Color` and coordinate ideas from this activity.
- Read the SFML tutorial on views and cameras (`sf::View`) to see how the
  coordinate system from question 5 can be scrolled, zoomed, or rotated
  independently of window size.
