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
echo "=== Stage 4: incremental rebuild (touch stats.h) ==="
make > /dev/null 2>&1 || fail "initial make failed"
touch stats.h
if make -q > /dev/null 2>&1; then
    fail "make did not detect that stats.h changed -- stats.h is missing from a .o prerequisite list"
fi
make > /dev/null 2>&1 || fail "make failed after touch stats.h"
./test_stats > /dev/null 2>&1 || fail "test_stats failed after incremental rebuild"
pass "incremental rebuild"

echo ""
echo "=== Stage 5: parallel build (make -j4) ==="
make clean > /dev/null 2>&1
make -j4 > /dev/null 2>&1 || fail "make -j4 failed"
test -f test_stats || fail "test_stats not found after make -j4"
./test_stats > /dev/null 2>&1 || fail "test_stats failed after make -j4"
pass "parallel build"

echo ""
echo "=== Stage 6: Makefile structure ==="
grep -q '\$@' Makefile && grep -q '\$<' Makefile \
    || fail "Makefile does not use both \$@ and \$<"
pass "automatic variables (\$@ and \$<)"

grep -qE '^CXXFLAGS\s*[+:]?=' Makefile && grep -q '\$(CXXFLAGS)' Makefile \
    || fail "Makefile does not define CXXFLAGS and use \$(CXXFLAGS)"
pass "CXXFLAGS defined and used"

grep -qE '^stats\.o\s*:.*stats\.h' Makefile \
    || fail "stats.o rule does not list stats.h as a prerequisite"
pass "header dependency (stats.o depends on stats.h)"

grep -q '\.PHONY' Makefile && grep '\.PHONY' Makefile | grep -q 'test' \
    && grep '\.PHONY' Makefile | grep -q 'clean' \
    || fail ".PHONY must list both 'test' and 'clean'"
pass ".PHONY declares test and clean"

make clean > /dev/null 2>&1 || fail "make clean failed"
make > /dev/null 2>&1 || fail "make failed"
output="$(make 2>&1)"
echo "$output" | grep -qi "nothing to be done\|is up to date" \
    || fail "make rebuilt targets after a fresh build -- real file targets (test_stats, stats.o, test_stats.o) must not appear in .PHONY"
pass "no spurious rebuilds on a second make"

echo ""
echo "=== Stage 7: cmake build ==="
rm -rf build
cmake -B build -DCMAKE_BUILD_TYPE=Release -Wno-dev 2>&1 | tail -3
cmake --build build 2>&1 | tail -3
pass "cmake build"

echo ""
echo "=== Stage 8: ctest ==="
ctest --test-dir build --output-on-failure
pass "ctest"

echo ""
echo "All visible checks passed."
echo ""
