// Visible Catch2 test suite for Media Library.
//
// Compile and run locally:
//   mkdir build && cd build
//   cmake .. -DSUBMISSION_DIR=<path-to-your-submission>
//   cmake --build .
//   ./media-library_tests

#include <catch2/catch_test_macros.hpp>
#include "media-library.hpp"

TEST_CASE("Book kind and summary", "[book]") {
    Book b("Dune", 1965, "Frank Herbert", 412);
    REQUIRE(b.kind() == "Book");
    REQUIRE(b.summary() == "Book: \"Dune\" (1965) by Frank Herbert, 412 pages");
}

TEST_CASE("Film kind and summary", "[film]") {
    Film f("Inception", 2010, "Christopher Nolan", 148);
    REQUIRE(f.kind() == "Film");
    REQUIRE(f.summary() ==
            "Film: \"Inception\" (2010), directed by Christopher Nolan, 148 min");
}

TEST_CASE("Album kind and summary", "[album]") {
    Album a("Thriller", 1982, "Michael Jackson", 9);
    REQUIRE(a.kind() == "Album");
    REQUIRE(a.summary() == "Album: \"Thriller\" (1982) by Michael Jackson, 9 tracks");
}

TEST_CASE("MediaItem shared accessors work through every derived type", "[shared]") {
    Book b("Dune", 1965, "Frank Herbert", 412);
    Film f("Inception", 2010, "Christopher Nolan", 148);
    REQUIRE(b.title() == "Dune");
    REQUIRE(b.year() == 1965);
    REQUIRE(f.title() == "Inception");
    REQUIRE(f.year() == 2010);
}

TEST_CASE("Library dispatches through base pointers", "[library]") {
    Library lib;
    Book b("Dune", 1965, "Frank Herbert", 412);
    Film f("Inception", 2010, "Christopher Nolan", 148);
    Album a("Thriller", 1982, "Michael Jackson", 9);

    lib.add(b);
    lib.add(f);
    lib.add(a);

    REQUIRE(lib.count() == 3);

    auto summaries = lib.summaries();
    REQUIRE(summaries.size() == 3);
    REQUIRE(summaries[0] == b.summary());
    REQUIRE(summaries[1] == f.summary());
    REQUIRE(summaries[2] == a.summary());
}

TEST_CASE("Library starts empty", "[library]") {
    Library lib;
    REQUIRE(lib.count() == 0);
    REQUIRE(lib.summaries().empty());
}
