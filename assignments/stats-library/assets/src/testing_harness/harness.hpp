// Do not modify this file.
#pragma once
#include <cmath>
#include <functional>
#include <iostream>
#include <string>
#include <vector>

namespace harness_detail {

struct TestCase {
    std::string name;
    std::function<void()> fn;
};

inline std::vector<TestCase>& registry() {
    static std::vector<TestCase> cases;
    return cases;
}

inline int& failure_count() {
    static int n = 0;
    return n;
}

inline int& check_count() {
    static int n = 0;
    return n;
}

struct Registrar {
    Registrar(const char* name, std::function<void()> fn) {
        registry().push_back({name, fn});
    }
};

inline int run_all() {
    for (auto& tc : registry()) {
        tc.fn();
    }
    int checks = check_count();
    int fails   = failure_count();
    if (fails == 0) {
        std::cout << checks << " check(s) passed\n";
        return 0;
    }
    return 1;
}

}  // namespace harness_detail

// Two-level expansion trick so __LINE__ is fully expanded before concatenation.
#define _HARNESS_TC_IMPL(test_name, uid) \
    static void _harness_body_##uid(); \
    static ::harness_detail::Registrar _harness_reg_##uid(test_name, _harness_body_##uid); \
    static void _harness_body_##uid()

#define _HARNESS_TC(test_name, uid) _HARNESS_TC_IMPL(test_name, uid)

#define TEST_CASE(name) _HARNESS_TC(name, __LINE__)

#define CHECK(expr) \
    do { \
        ++::harness_detail::check_count(); \
        if (!(expr)) { \
            ++::harness_detail::failure_count(); \
            std::cerr << "FAIL: " << #expr \
                      << "  (" << __FILE__ << ":" << __LINE__ << ")\n"; \
        } \
    } while (0)

#define CHECK_CLOSE(a, b, eps) \
    do { \
        ++::harness_detail::check_count(); \
        double _hca = static_cast<double>(a); \
        double _hcb = static_cast<double>(b); \
        double _hce = static_cast<double>(eps); \
        if (std::fabs(_hca - _hcb) > _hce) { \
            ++::harness_detail::failure_count(); \
            std::cerr << "FAIL: CHECK_CLOSE(" << #a << ", " << #b \
                      << ", " << #eps \
                      << ")  got " << _hca << " vs " << _hcb \
                      << "  (" << __FILE__ << ":" << __LINE__ << ")\n"; \
        } \
    } while (0)

#define RUN_ALL_TESTS() ::harness_detail::run_all()
