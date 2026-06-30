#include "operations.hpp"
#include <algorithm>
#include <cmath>

// Helper: clamp a value to [0, 255]
static uint8_t clamp(int v) {
    if (v < 0)   return 0;
    if (v > 255) return 255;
    return static_cast<uint8_t>(v);
}

static uint8_t clampf(float v) {
    if (v < 0.0f)   return 0;
    if (v > 255.0f) return 255;
    return static_cast<uint8_t>(std::round(v));
}

void op_multiply(TGAImage& image, const TGAImage& layer) {
    // TODO: for each pixel i:
    //   result.red   = clamp(round((image[i].red   * layer[i].red)   / 255.0))
    //   result.green = clamp(round((image[i].green * layer[i].green) / 255.0))
    //   result.blue  = clamp(round((image[i].blue  * layer[i].blue)  / 255.0))
}

void op_subtract(TGAImage& image, const TGAImage& layer) {
    // TODO: for each pixel i:
    //   result.red   = clamp(image[i].red   - layer[i].red)
    //   result.green = clamp(image[i].green - layer[i].green)
    //   result.blue  = clamp(image[i].blue  - layer[i].blue)
}

void op_screen(TGAImage& image, const TGAImage& layer) {
    // TODO: for each pixel i, per channel:
    //   result = 255 - clamp(round(((255 - A) * (255 - B)) / 255.0))
}

void op_overlay(TGAImage& image, const TGAImage& layer) {
    // TODO: for each pixel i, per channel:
    //   if base <= 127:
    //     result = clamp(round(2 * base * blend / 255.0))
    //   else:
    //     result = 255 - clamp(round(2 * (255-base) * (255-blend) / 255.0))
}

void op_combine(TGAImage& image,
                const TGAImage& red_src,
                const TGAImage& green_src,
                const TGAImage& blue_src) {
    // TODO: for each pixel i:
    //   image[i].red   = red_src[i].red
    //   image[i].green = green_src[i].green
    //   image[i].blue  = blue_src[i].blue
}

void op_flip(TGAImage& image) {
    // TODO: reverse the row order of image.pixels
    // (row 0 becomes the last row, etc.)
}

void op_only_red(TGAImage& image) {
    // TODO: set green = 0, blue = 0 for every pixel
}

void op_only_green(TGAImage& image) {
    // TODO: set red = 0, blue = 0 for every pixel
}

void op_only_blue(TGAImage& image) {
    // TODO: set red = 0, green = 0 for every pixel
}

void op_add_red(TGAImage& image, int amount) {
    // TODO: add `amount` to red channel of every pixel, clamp to [0,255]
}

void op_add_green(TGAImage& image, int amount) {
    // TODO: add `amount` to green channel of every pixel, clamp to [0,255]
}

void op_add_blue(TGAImage& image, int amount) {
    // TODO: add `amount` to blue channel of every pixel, clamp to [0,255]
}

void op_scale_red(TGAImage& image, float factor) {
    // TODO: multiply red channel of every pixel by `factor`, clamp to [0,255]
}

void op_scale_green(TGAImage& image, float factor) {
    // TODO: multiply green channel of every pixel by `factor`, clamp to [0,255]
}

void op_scale_blue(TGAImage& image, float factor) {
    // TODO: multiply blue channel of every pixel by `factor`, clamp to [0,255]
}

// ---- Extra credit ----

void op_blur(TGAImage& image, int radius) {
    // TODO: implement Gaussian blur with radius `radius`, sigma = radius / 2.0
    // Build the kernel, convolve 2D, clamp output
}

void op_sharpen(TGAImage& image, int radius) {
    // TODO: unsharp mask: blurred = blur(image, radius)
    //       result = clamp(2 * image - blurred) per channel
}

void op_edge(TGAImage& image) {
    // TODO: convert to grayscale, apply Sobel X and Y kernels,
    //       compute magnitude sqrt(Gx^2 + Gy^2), store as grayscale
}

void op_sepia(TGAImage& image) {
    // TODO: apply sepia matrix per pixel:
    //   R_out = clamp(0.393*R + 0.769*G + 0.189*B)
    //   G_out = clamp(0.349*R + 0.686*G + 0.168*B)
    //   B_out = clamp(0.272*R + 0.534*G + 0.131*B)
}
