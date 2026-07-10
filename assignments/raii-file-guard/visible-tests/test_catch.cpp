#include <catch2/catch_test_macros.hpp>
#include "file_guard.hpp"

#include <cstdio>
#include <string>

namespace {

// Returns a path inside the test binary's working directory. Catch2 tests
// run from the build directory, so plain relative names are fine here.
std::string temp_path(const char* name) {
    return std::string("visible_") + name;
}

} // namespace

TEST_CASE("Write mode creates a file and is_open is true", "[visible]") {
    std::string path = temp_path("create.txt");
    std::remove(path.c_str());
    FileGuard g(path.c_str(), Mode::Write);
    REQUIRE(g.is_open());
    REQUIRE(g.fd() >= 0);
}

TEST_CASE("Read mode on a nonexistent file fails to open", "[visible]") {
    FileGuard g("this_path_should_not_exist_12345.txt", Mode::Read);
    REQUIRE_FALSE(g.is_open());
    REQUIRE(g.fd() == -1);
}

TEST_CASE("write_all then read_all round-trips the content", "[visible]") {
    std::string path = temp_path("roundtrip.txt");
    std::remove(path.c_str());
    {
        FileGuard g(path.c_str(), Mode::Write);
        REQUIRE(g.is_open());
        const char* msg = "hello, raii";
        long n = g.write_all(msg, static_cast<long>(std::string(msg).size()));
        REQUIRE(n == static_cast<long>(std::string(msg).size()));
    }
    {
        FileGuard g(path.c_str(), Mode::Read);
        REQUIRE(g.is_open());
        std::string contents = g.read_all();
        REQUIRE(contents == "hello, raii");
    }
    std::remove(path.c_str());
}

TEST_CASE("close is idempotent and fd becomes -1", "[visible]") {
    std::string path = temp_path("close.txt");
    std::remove(path.c_str());
    FileGuard g(path.c_str(), Mode::Write);
    REQUIRE(g.is_open());
    g.close();
    REQUIRE_FALSE(g.is_open());
    REQUIRE(g.fd() == -1);
    g.close(); // second call must be a no-op, not a crash
    REQUIRE_FALSE(g.is_open());
    std::remove(path.c_str());
}

TEST_CASE("read_some returns a partial read from a small buffer", "[visible]") {
    std::string path = temp_path("partial.txt");
    std::remove(path.c_str());
    {
        FileGuard g(path.c_str(), Mode::Write);
        const char* msg = "0123456789";
        g.write_all(msg, 10);
    }
    {
        FileGuard g(path.c_str(), Mode::Read);
        char buf[4] = {};
        long n = g.read_some(buf, 4);
        REQUIRE(n == 4);
        REQUIRE(std::string(buf, 4) == "0123");
    }
    std::remove(path.c_str());
}

TEST_CASE("Append mode adds to existing content instead of truncating", "[visible]") {
    std::string path = temp_path("append.txt");
    std::remove(path.c_str());
    {
        FileGuard g(path.c_str(), Mode::Write);
        g.write_all("abc", 3);
    }
    {
        FileGuard g(path.c_str(), Mode::Append);
        g.write_all("def", 3);
    }
    {
        FileGuard g(path.c_str(), Mode::Read);
        REQUIRE(g.read_all() == "abcdef");
    }
    std::remove(path.c_str());
}
