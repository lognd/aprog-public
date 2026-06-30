#pragma once
#include <cstdint>
#include <string>
#include <vector>

// #pragma pack(push, 1) tells the compiler to pack struct fields with NO padding bytes
// between them. Normally the compiler inserts padding to align fields to their
// natural alignment (e.g., a uint16_t on a 2-byte boundary). For a binary file
// format like TGA, we need the struct to match the file layout exactly -- no
// padding allowed. #pragma pack(pop) restores the default packing rules.
#pragma pack(push, 1)
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

static_assert(sizeof(TGAHeader) == 18, "TGAHeader must be exactly 18 bytes");

// TGA stores pixels in Blue-Green-Red order, not RGB.
struct Pixel {
    uint8_t blue;
    uint8_t green;
    uint8_t red;
};

static_assert(sizeof(Pixel) == 3, "Pixel must be exactly 3 bytes");

class TGAImage {
public:
    TGAHeader header{};
    std::vector<Pixel> pixels;

    // Read a TGA file. Returns false if the file cannot be opened.
    bool read(const std::string& filename);

    // Write a TGA file. Returns false if the file cannot be written.
    bool write(const std::string& filename) const;

    int width() const  { return header.width; }
    int height() const { return header.height; }
};
