#!/usr/bin/env bash
# Run visible tests for hex-dump.
# Build first:
#   mkdir -p build && cd build && cmake .. && make && cd ..
set -uo pipefail

BINARY="${1:-./build/hexdump}"
TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0

check() {
    local name="$1"
    local sample="$2"
    local expected="$3"

    if ! "$BINARY" "$sample" > /tmp/hexdump_actual_output 2>/dev/null; then
        echo "FAIL: $name (nonzero exit)"
        FAIL=$((FAIL + 1))
        return
    fi

    if diff -q /tmp/hexdump_actual_output "$expected" > /dev/null 2>&1; then
        echo "PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "FAIL: $name"
        echo "  Expected:"
        sed 's/^/    /' "$expected"
        echo "  Got:"
        sed 's/^/    /' /tmp/hexdump_actual_output
        FAIL=$((FAIL + 1))
    fi
}

check "ascii_text" \
    "$TESTS_DIR/samples/ascii.bin" \
    "$TESTS_DIR/expected/ascii.txt"

check "binary_non_printable" \
    "$TESTS_DIR/samples/binary.bin" \
    "$TESTS_DIR/expected/binary.txt"

check "exact_16_bytes" \
    "$TESTS_DIR/samples/exact16.bin" \
    "$TESTS_DIR/expected/exact16.txt"

check "empty_file" \
    "$TESTS_DIR/samples/empty.bin" \
    "$TESTS_DIR/expected/empty.txt"

# Missing file: expect a message on stderr and a nonzero exit code.
if "$BINARY" "$TESTS_DIR/samples/does-not-exist.bin" 2>/tmp/hexdump_missing_stderr; then
    echo "FAIL: missing_file (expected nonzero exit)"
    FAIL=$((FAIL + 1))
elif [ ! -s /tmp/hexdump_missing_stderr ]; then
    echo "FAIL: missing_file (expected a message on stderr)"
    FAIL=$((FAIL + 1))
else
    echo "PASS: missing_file"
    PASS=$((PASS + 1))
fi
rm -f /tmp/hexdump_missing_stderr

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
