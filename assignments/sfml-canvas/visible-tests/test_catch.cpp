// Visible Catch2 tests for SFML Canvas.
//
// These tests are entirely self-contained -- no reference PNGs required --
// so students can copy this file and run it locally after installing SFML.
#include <catch2/catch_test_macros.hpp>
#include "canvas.hpp"

#include <cstdint>

namespace {

// round-half-up, matching the spec in canvas.hpp -- used to compute expected
// values by hand in these tests.
std::uint8_t expected_channel(float value) {
    return static_cast<std::uint8_t>(value + 0.5f);
}

}  // namespace

TEST_CASE("make_gradient endpoints match from/to exactly", "[gradient]") {
    sf::Image img = make_gradient(11, 3, sf::Color(0, 0, 0, 255), sf::Color(100, 200, 255, 255));
    REQUIRE(img.getSize().x == 11);
    REQUIRE(img.getSize().y == 3);
    REQUIRE(img.getPixel({0, 0}) == sf::Color(0, 0, 0, 255));
    REQUIRE(img.getPixel({10, 0}) == sf::Color(100, 200, 255, 255));
}

TEST_CASE("make_gradient is uniform down every column", "[gradient]") {
    sf::Image img = make_gradient(5, 4, sf::Color::Black, sf::Color::White);
    sf::Color col2 = img.getPixel({2, 0});
    for (unsigned y = 1; y < 4; ++y) {
        REQUIRE(img.getPixel({2, y}) == col2);
    }
}

TEST_CASE("make_gradient midpoint rounds per spec", "[gradient]") {
    // width = 3 -> x=1 gives t = 1/2 exactly.
    sf::Image img = make_gradient(3, 1, sf::Color(0, 0, 0, 255), sf::Color(9, 10, 11, 255));
    sf::Color mid = img.getPixel({1, 0});
    REQUIRE(mid.r == expected_channel(4.5f));
    REQUIRE(mid.g == expected_channel(5.0f));
    REQUIRE(mid.b == expected_channel(5.5f));
}

TEST_CASE("checkerboard alternates by block", "[checkerboard]") {
    sf::Image img = checkerboard(8, 8, 2, sf::Color::Black, sf::Color::White);
    REQUIRE(img.getPixel({0, 0}) == sf::Color::Black);
    REQUIRE(img.getPixel({1, 0}) == sf::Color::Black);
    REQUIRE(img.getPixel({2, 0}) == sf::Color::White);
    REQUIRE(img.getPixel({3, 0}) == sf::Color::White);
    REQUIRE(img.getPixel({0, 2}) == sf::Color::White);
}

TEST_CASE("draw_disk center pixel is always painted", "[disk]") {
    sf::Image img;
    img.resize({20, 20}, sf::Color::White);
    draw_disk(img, 10, 10, 5, sf::Color::Red);
    REQUIRE(img.getPixel({10, 10}) == sf::Color::Red);
    REQUIRE(img.getPixel({0, 0}) == sf::Color::White);
}

TEST_CASE("draw_disk uses a circular boundary, not a square", "[disk]") {
    sf::Image img;
    img.resize({20, 20}, sf::Color::White);
    draw_disk(img, 10, 10, 5, sf::Color::Red);
    // A far corner of the bounding SQUARE (offset 5,5 -> distance^2 = 50 > 25)
    // must NOT be painted for a true circle.
    REQUIRE(img.getPixel({15, 15}) == sf::Color::White);
    // A point on the axis at exactly the radius must be painted.
    REQUIRE(img.getPixel({15, 10}) == sf::Color::Red);
}

TEST_CASE("draw_disk clips at image edges without crashing", "[disk]") {
    sf::Image img;
    img.resize({10, 10}, sf::Color::White);
    draw_disk(img, 0, 0, 5, sf::Color::Blue);
    REQUIRE(img.getPixel({0, 0}) == sf::Color::Blue);
    REQUIRE(img.getSize().x == 10);
    REQUIRE(img.getSize().y == 10);
}

TEST_CASE("blend at alpha 0 reproduces base exactly", "[blend]") {
    sf::Image base = checkerboard(6, 6, 2, sf::Color::Red, sf::Color::Blue);
    sf::Image overlay = checkerboard(6, 6, 2, sf::Color::Green, sf::Color::Yellow);
    sf::Image result = blend(base, overlay, 0.f);
    for (unsigned y = 0; y < 6; ++y) {
        for (unsigned x = 0; x < 6; ++x) {
            REQUIRE(result.getPixel({x, y}) == base.getPixel({x, y}));
        }
    }
}

TEST_CASE("blend at alpha 1 reproduces overlay exactly", "[blend]") {
    sf::Image base = checkerboard(6, 6, 2, sf::Color::Red, sf::Color::Blue);
    sf::Image overlay = checkerboard(6, 6, 2, sf::Color::Green, sf::Color::Yellow);
    sf::Image result = blend(base, overlay, 1.f);
    for (unsigned y = 0; y < 6; ++y) {
        for (unsigned x = 0; x < 6; ++x) {
            REQUIRE(result.getPixel({x, y}) == overlay.getPixel({x, y}));
        }
    }
}

TEST_CASE("blend at alpha 0.5 rounds per spec", "[blend]") {
    sf::Image base;
    base.resize({1, 1}, sf::Color(0, 0, 0, 255));
    sf::Image overlay;
    overlay.resize({1, 1}, sf::Color(9, 10, 11, 255));
    sf::Image result = blend(base, overlay, 0.5f);
    sf::Color px = result.getPixel({0, 0});
    REQUIRE(px.r == expected_channel(4.5f));
    REQUIRE(px.g == expected_channel(5.0f));
    REQUIRE(px.b == expected_channel(5.5f));
}

TEST_CASE("outline_rect paints only the border, not the interior", "[outline]") {
    sf::Image img;
    img.resize({10, 10}, sf::Color::White);
    outline_rect(img, 2, 2, 4, 4, sf::Color::Black);
    // Corners and edge midpoints of the border.
    REQUIRE(img.getPixel({2, 2}) == sf::Color::Black);
    REQUIRE(img.getPixel({5, 2}) == sf::Color::Black);
    REQUIRE(img.getPixel({2, 5}) == sf::Color::Black);
    REQUIRE(img.getPixel({5, 5}) == sf::Color::Black);
    // Interior stays untouched.
    REQUIRE(img.getPixel({3, 3}) == sf::Color::White);
    REQUIRE(img.getPixel({4, 4}) == sf::Color::White);
}

TEST_CASE("outline_rect clips at image edges without crashing", "[outline]") {
    sf::Image img;
    img.resize({5, 5}, sf::Color::White);
    // Rect spans x,y in [-2, 5): border columns are x = -2 (fully off-image,
    // clipped away) and x = 4 (the image's last column); same for rows.
    outline_rect(img, -2, -2, 7, 7, sf::Color::Black);
    REQUIRE(img.getPixel({4, 4}) == sf::Color::Black);
    REQUIRE(img.getPixel({0, 0}) == sf::Color::White);
    REQUIRE(img.getSize().x == 5);
    REQUIRE(img.getSize().y == 5);
}
