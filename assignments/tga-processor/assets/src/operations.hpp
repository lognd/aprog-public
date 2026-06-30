#pragma once
#include "tga.hpp"

// All operations modify `image` in place.
// Two-image operations read from `layer` (the second image).

void op_multiply(TGAImage& image, const TGAImage& layer);
void op_subtract(TGAImage& image, const TGAImage& layer);
void op_screen(TGAImage& image, const TGAImage& layer);
void op_overlay(TGAImage& image, const TGAImage& layer);
void op_combine(TGAImage& image,
                const TGAImage& red_src,
                const TGAImage& green_src,
                const TGAImage& blue_src);

void op_flip(TGAImage& image);

void op_only_red(TGAImage& image);
void op_only_green(TGAImage& image);
void op_only_blue(TGAImage& image);

void op_add_red(TGAImage& image, int amount);
void op_add_green(TGAImage& image, int amount);
void op_add_blue(TGAImage& image, int amount);

void op_scale_red(TGAImage& image, float factor);
void op_scale_green(TGAImage& image, float factor);
void op_scale_blue(TGAImage& image, float factor);

// Extra credit
void op_blur(TGAImage& image, int radius);
void op_sharpen(TGAImage& image, int radius);
void op_edge(TGAImage& image);
void op_sepia(TGAImage& image);
