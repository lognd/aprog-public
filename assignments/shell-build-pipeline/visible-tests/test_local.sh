#!/bin/bash
# Local test script for shell-build-pipeline.
# Run from the directory containing build.sh and the .cpp/.h files.
#
# Usage:
#   bash visible-tests/test_local.sh
#   (or copy this script into the same directory as build.sh and run it there)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(pwd)"

pass=0
fail=0

ok()   { echo "PASS: $1"; pass=$((pass+1)); }
fail() { echo "FAIL: $1"; fail=$((fail+1)); }

mtime() { stat -c %Y "$1" 2>/dev/null || echo 0; }

# ---------------------------------------------------------------------------
# Test 1: build.sh exists
# ---------------------------------------------------------------------------
if [ -f "$WORK_DIR/build.sh" ]; then
    ok "build.sh exists"
else
    fail "build.sh not found -- copy assets into this directory first"
    echo ""
    echo "No build.sh found. Aborting."
    exit 1
fi

# ---------------------------------------------------------------------------
# Test 2: full build produces program
# ---------------------------------------------------------------------------
rm -f *.i *.s *.o program build.log
bash build.sh
if [ -f program ]; then
    ok "build produces ./program"
else
    fail "build did not produce ./program"
    echo ""; echo "Build failed. Aborting remaining tests."; exit 1
fi

# ---------------------------------------------------------------------------
# Test 3: program output is correct
# ---------------------------------------------------------------------------
OUTPUT=$(./program)
EXPECTED="Hello, world!
answer: 42
passphrase: STAGES_COMPLETE"
if [ "$OUTPUT" = "$EXPECTED" ]; then
    ok "program output is correct"
else
    fail "program output mismatch"
    echo "  expected: $EXPECTED"
    echo "  got:      $OUTPUT"
fi

# ---------------------------------------------------------------------------
# Test 4: build.log is created (redirection check)
# ---------------------------------------------------------------------------
if [ -f build.log ]; then
    ok "build.log created by redirection"
else
    fail "build.log not found -- redirect stderr to build.log"
fi

# ---------------------------------------------------------------------------
# Test 5: pipe present in script
# ---------------------------------------------------------------------------
if grep -q '|' build.sh; then
    ok "build.sh uses at least one pipe"
else
    fail "no pipe found in build.sh"
fi

# ---------------------------------------------------------------------------
# Test 6: all four stages present
# ---------------------------------------------------------------------------
missing=0
for flag in '-E' '-S' '-c'; do
    if ! grep -qF "g++ $flag" build.sh; then
        fail "g++ $flag not found in build.sh"
        missing=$((missing+1))
    fi
done
[ "$missing" -eq 0 ] && ok "all four g++ stages present in build.sh"

# ---------------------------------------------------------------------------
# Test 7: incremental -- touching greet.cpp only rebuilds its chain
# ---------------------------------------------------------------------------
old_greet_o=$(mtime greet.o)
old_main_o=$(mtime main.o)
old_math_o=$(mtime math_utils.o)
old_program=$(mtime program)
sleep 1
touch greet.cpp
bash build.sh >/dev/null 2>&1
new_greet_o=$(mtime greet.o)
new_main_o=$(mtime main.o)
new_math_o=$(mtime math_utils.o)
new_program=$(mtime program)

if [ "$new_greet_o" -gt "$old_greet_o" ]; then
    ok "greet.o is rebuilt after touching greet.cpp"
else
    fail "greet.o was not rebuilt after touching greet.cpp"
fi

if [ "$new_main_o" -eq "$old_main_o" ]; then
    ok "main.o is NOT rebuilt when only greet.cpp changes"
else
    fail "main.o was unnecessarily rebuilt"
fi

if [ "$new_math_o" -eq "$old_math_o" ]; then
    ok "math_utils.o is NOT rebuilt when only greet.cpp changes"
else
    fail "math_utils.o was unnecessarily rebuilt"
fi

if [ "$new_program" -gt "$old_program" ]; then
    ok "program is relinked after greet.cpp changes"
else
    fail "program was not relinked after greet.cpp changed"
fi

# ---------------------------------------------------------------------------
# Test 8: incremental -- nothing rebuilt when nothing changed
# ---------------------------------------------------------------------------
old_greet_o=$(mtime greet.o)
old_main_o=$(mtime main.o)
old_math_o=$(mtime math_utils.o)
old_program=$(mtime program)
sleep 1
bash build.sh >/dev/null 2>&1
new_greet_o=$(mtime greet.o)
new_main_o=$(mtime main.o)
new_math_o=$(mtime math_utils.o)
new_program=$(mtime program)

if [ "$new_greet_o" -eq "$old_greet_o" ] && \
   [ "$new_main_o" -eq "$old_main_o" ]   && \
   [ "$new_math_o" -eq "$old_math_o" ]   && \
   [ "$new_program" -eq "$old_program" ]; then
    ok "nothing is rebuilt when nothing changed"
else
    fail "files were rebuilt even though nothing changed"
fi

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
echo ""
echo "passed: $pass  |  failed: $fail"
