#include <catch2/catch_test_macros.hpp>
#include "matrix.hpp"
#include <cstring>

// Helper: allocate and fill a matrix from a flat initializer list.
// Caller is responsible for delete[].
static int* make_mat(std::initializer_list<int> vals) {
    int* m = new int[vals.size()];
    int i = 0;
    for (int v : vals) m[i++] = v;
    return m;
}

TEST_CASE("mat_get reads correct element", "[visible][get]") {
    // 2x3:  1 2 3
    //       4 5 6
    int* m = make_mat({1, 2, 3, 4, 5, 6});
    REQUIRE(mat_get(m, 3, 0, 0) == 1);
    REQUIRE(mat_get(m, 3, 0, 2) == 3);
    REQUIRE(mat_get(m, 3, 1, 0) == 4);
    REQUIRE(mat_get(m, 3, 1, 2) == 6);
    delete[] m;
}

TEST_CASE("mat_set writes correct element", "[visible][set]") {
    int* m = make_mat({0, 0, 0, 0});
    mat_set(m, 2, 0, 1, 99);
    REQUIRE(m[1] == 99);
    mat_set(m, 2, 1, 0, 42);
    REQUIRE(m[2] == 42);
    delete[] m;
}

TEST_CASE("mat_fill sets all elements", "[visible][fill]") {
    int* m = new int[6];
    mat_fill(m, 2, 3, 7);
    for (int i = 0; i < 6; ++i) REQUIRE(m[i] == 7);
    delete[] m;
}

TEST_CASE("mat_add sums element-wise", "[visible][add]") {
    int* a   = make_mat({1, 2, 3, 4});
    int* b   = make_mat({10, 20, 30, 40});
    int* dst = new int[4];
    mat_add(a, b, dst, 2, 2);
    REQUIRE(dst[0] == 11);
    REQUIRE(dst[1] == 22);
    REQUIRE(dst[2] == 33);
    REQUIRE(dst[3] == 44);
    delete[] a; delete[] b; delete[] dst;
}

TEST_CASE("mat_transpose square", "[visible][transpose]") {
    // 2x2:  1 2
    //       3 4
    // T:    1 3
    //       2 4
    int* src = make_mat({1, 2, 3, 4});
    int* dst = new int[4];
    mat_transpose(src, dst, 2, 2);
    REQUIRE(dst[0] == 1);
    REQUIRE(dst[1] == 3);
    REQUIRE(dst[2] == 2);
    REQUIRE(dst[3] == 4);
    delete[] src; delete[] dst;
}

TEST_CASE("mat_transpose non-square", "[visible][transpose]") {
    // src 2x3:  1 2 3
    //           4 5 6
    // dst 3x2:  1 4
    //           2 5
    //           3 6
    int* src = make_mat({1, 2, 3, 4, 5, 6});
    int* dst = new int[6];
    mat_transpose(src, dst, 2, 3);
    REQUIRE(dst[0] == 1); REQUIRE(dst[1] == 4);
    REQUIRE(dst[2] == 2); REQUIRE(dst[3] == 5);
    REQUIRE(dst[4] == 3); REQUIRE(dst[5] == 6);
    delete[] src; delete[] dst;
}

TEST_CASE("mat_row_sum", "[visible][sum]") {
    // 2x3:  1 2 3
    //       4 5 6
    int* m = make_mat({1, 2, 3, 4, 5, 6});
    REQUIRE(mat_row_sum(m, 3, 0) == 6);
    REQUIRE(mat_row_sum(m, 3, 1) == 15);
    delete[] m;
}

TEST_CASE("mat_col_sum", "[visible][sum]") {
    // 2x3:  1 2 3
    //       4 5 6
    int* m = make_mat({1, 2, 3, 4, 5, 6});
    REQUIRE(mat_col_sum(m, 2, 3, 0) == 5);
    REQUIRE(mat_col_sum(m, 2, 3, 1) == 7);
    REQUIRE(mat_col_sum(m, 2, 3, 2) == 9);
    delete[] m;
}

TEST_CASE("mat_is_symmetric true", "[visible][symmetric]") {
    // 3x3 symmetric:
    //   1 2 3
    //   2 4 5
    //   3 5 6
    int* m = make_mat({1, 2, 3, 2, 4, 5, 3, 5, 6});
    REQUIRE(mat_is_symmetric(m, 3) == true);
    delete[] m;
}

TEST_CASE("mat_is_symmetric false", "[visible][symmetric]") {
    // 2x2 not symmetric:  1 2
    //                     3 4
    int* m = make_mat({1, 2, 3, 4});
    REQUIRE(mat_is_symmetric(m, 2) == false);
    delete[] m;
}
