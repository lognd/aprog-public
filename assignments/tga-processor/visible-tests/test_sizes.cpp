#include <catch2/catch_test_macros.hpp>
#include "tga.hpp"

TEST_CASE("TGAHeader is exactly 18 bytes", "[struct-size]") {
    REQUIRE(sizeof(TGAHeader) == 18);
}

TEST_CASE("Pixel is exactly 3 bytes", "[struct-size]") {
    REQUIRE(sizeof(Pixel) == 3);
}

TEST_CASE("Pixel field order is blue-green-red", "[struct-layout]") {
    Pixel p{};
    char* base = reinterpret_cast<char*>(&p);
    char* b    = reinterpret_cast<char*>(&p.blue);
    char* g    = reinterpret_cast<char*>(&p.green);
    char* r    = reinterpret_cast<char*>(&p.red);
    REQUIRE(b - base == 0);
    REQUIRE(g - base == 1);
    REQUIRE(r - base == 2);
}
