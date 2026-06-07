#!/usr/bin/env bash
# Run this script from the directory containing your Makefile and CMakeLists.txt
# to check your work before submitting.
#
# Usage:  bash visible-tests/check.sh
#         (run from the project root, not from visible-tests/)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

pass() { printf "  PASS  %s\n" "$1"; }
fail() { printf "  FAIL  %s\n" "$1"; exit 1; }

echo ""
echo "=== Stage 1: make ==="
make 2>&1 | tail -5
test -f test_stats || fail "test_stats not found after make"
pass "make"

echo ""
echo "=== Stage 2: make test ==="
make test | grep "All tests passed" || fail "make test did not print expected output"
pass "make test"

echo ""
echo "=== Stage 3: make clean ==="
make clean
count=$(find . -maxdepth 1 \( -name "*.o" -o -name "*.a" -o -name "test_stats" \) | wc -l)
test "$count" -eq 0 || fail "make clean left behind: $(ls *.o *.a test_stats 2>/dev/null)"
pass "make clean"

echo ""
echo "=== Stage 4: cmake build ==="
cmake -B build -DCMAKE_BUILD_TYPE=Release -Wno-dev 2>&1 | tail -3
cmake --build build 2>&1 | tail -3
pass "cmake build"

echo ""
echo "=== Stage 5: ctest ==="
ctest --test-dir build --output-on-failure
pass "ctest"

echo ""
echo "All visible checks passed."
echo ""
