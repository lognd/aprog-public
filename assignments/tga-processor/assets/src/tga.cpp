#include "tga.hpp"
#include <fstream>

bool TGAImage::read(const std::string& filename) {
    // TODO: open the file in binary mode (std::ios::binary)
    // TODO: read sizeof(TGAHeader) bytes into this->header
    // TODO: compute pixel_count = header.width * header.height
    // TODO: resize this->pixels to pixel_count
    // TODO: read pixel_count * sizeof(Pixel) bytes into this->pixels.data()
    // TODO: return false if any open/read fails, true on success
    return false;
}

bool TGAImage::write(const std::string& filename) const {
    // TODO: open the file for writing in binary mode
    // TODO: write sizeof(TGAHeader) bytes from this->header
    // TODO: write pixels.size() * sizeof(Pixel) bytes from this->pixels.data()
    // TODO: return false if any write fails, true on success
    return false;
}
