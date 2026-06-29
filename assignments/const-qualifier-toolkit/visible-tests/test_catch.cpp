#include <catch2/catch_test_macros.hpp>
#include "grid.hpp"

// 3x3 grid:
//  A B C
//  D E F
//  G H I
static const char G3[9] = {'A','B','C','D','E','F','G','H','I'};

TEST_CASE("cell_at returns correct character", "[visible]") {
    REQUIRE(cell_at(G3, 3, 0, 0) == 'A');
    REQUIRE(cell_at(G3, 3, 0, 2) == 'C');
    REQUIRE(cell_at(G3, 3, 1, 1) == 'E');
    REQUIRE(cell_at(G3, 3, 2, 2) == 'I');
}

TEST_CASE("count_cells counts matching characters", "[visible]") {
    const char g[9] = {'X','O','X','O','X','O','X','O','X'};
    REQUIRE(count_cells(g, 3, 3, 'X') == 5);
    REQUIRE(count_cells(g, 3, 3, 'O') == 4);
    REQUIRE(count_cells(g, 3, 3, '.') == 0);
}

TEST_CASE("grids_equal compares two grids correctly", "[visible]") {
    const char a[4] = {'A','B','C','D'};
    const char b[4] = {'A','B','C','D'};
    const char c[4] = {'A','B','C','X'};
    REQUIRE(grids_equal(a, b, 2, 2) == true);
    REQUIRE(grids_equal(a, c, 2, 2) == false);
}

TEST_CASE("fill_grid sets all cells", "[visible]") {
    char g[6] = {};
    fill_grid(g, 2, 3, '.');
    for (int i = 0; i < 6; ++i)
        REQUIRE(g[i] == '.');
    fill_grid(g, 2, 3, 'Z');
    for (int i = 0; i < 6; ++i)
        REQUIRE(g[i] == 'Z');
}

TEST_CASE("row_ptr points into the original array", "[visible]") {
    const char* r1 = row_ptr(G3, 3, 1);
    // row 1 starts at index 3
    REQUIRE(r1 == G3 + 3);
    REQUIRE(*r1 == 'D');
    REQUIRE(r1[2] == 'F');
}
