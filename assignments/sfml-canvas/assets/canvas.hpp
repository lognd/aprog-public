// Fixed header for the SFML Canvas assignment. Do not modify.
//
// Every function here works with sf::Image, an in-memory grid of pixels
// (sf::Color values, one per pixel) that lives entirely on the CPU. There
// is no window, no GPU, and no event loop involved anywhere in this file --
// see the assignment README for why that is a deliberate choice.
#pragma once

#include <SFML/Graphics.hpp>

// make_gradient: build a width x height image whose column x is a linear
// interpolation between `from` (at x = 0) and `to` (at x = width - 1),
// computed independently per channel (r, g, b, a). Every row is identical
// (the same color repeated down every column). If width <= 1, every pixel
// is `from`.
//
// Per-channel rounding rule (applies to every function below that produces
// a new channel value from a fractional computation): round to the nearest
// integer using round-half-up, i.e.
//     channel = static_cast<sf::Uint8>(value + 0.5f)
// where `value` is the exact (double/float) computed channel value before
// rounding.
sf::Image make_gradient(unsigned width, unsigned height, sf::Color from, sf::Color to);

// checkerboard: tile a width x height image into cell x cell blocks that
// alternate between color a and color b. Block (0, 0) -- the block
// containing pixel (0, 0) -- is color a. In general, the pixel at (x, y)
// belongs to block (x / cell, y / cell) (integer division); if the sum of
// those two block indices is even, the pixel is color a, otherwise color b.
sf::Image checkerboard(unsigned width, unsigned height, unsigned cell, sf::Color a, sf::Color b);

// draw_disk: paint a filled circle of radius r, centered at pixel (cx, cy),
// directly onto img (img is not resized). A pixel (px, py) is part of the
// disk exactly when (px - cx)*(px - cx) + (py - cy)*(py - cy) <= r*r. Any
// part of the disk that would fall outside img's bounds is simply skipped
// (clipped) -- do not write outside [0, img.getSize().x) x [0, img.getSize().y).
void draw_disk(sf::Image& img, int cx, int cy, int r, sf::Color color);

// blend: per-pixel convex combination of two same-size images:
//     result_channel = base_channel * (1 - alpha) + overlay_channel * alpha
// applied independently to each of r, g, b, a, then rounded per the
// round-half-up rule documented on make_gradient. alpha = 0 reproduces
// base exactly; alpha = 1 reproduces overlay exactly. base and overlay are
// always the same size in every graded case; the returned image has that
// same size.
sf::Image blend(const sf::Image& base, const sf::Image& overlay, float alpha);

// outline_rect: draw a 1-pixel-wide border directly onto img, tracing the
// rectangle whose pixels span [x, x + w) horizontally and [y, y + h)
// vertically: the top row (y), the bottom row (y + h - 1), the left column
// (x), and the right column (x + w - 1) of that span. Does not fill the
// interior. Any border pixel that would fall outside img's bounds is
// simply skipped (clipped).
void outline_rect(sf::Image& img, int x, int y, int w, int h, sf::Color color);
