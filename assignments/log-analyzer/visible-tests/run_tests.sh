#!/usr/bin/env bash
# Run visible tests for log-analyzer.
# Compile first: g++ -std=c++17 -Wall -Wextra -o log-analyzer log-analyzer.cpp
set -euo pipefail

BINARY="${1:-./log-analyzer}"
TESTS_DIR="$(cd "$(dirname "$0")" && pwd)"
PASS=0
FAIL=0

check() {
    local name="$1"
    local log="$2"
    local expected="$3"
    local actual
    actual=$("$BINARY" "$log" 2>/dev/null || true)
    if [ "$actual" = "$expected" ]; then
        echo "PASS: $name"
        PASS=$((PASS + 1))
    else
        echo "FAIL: $name"
        echo "  Expected:"
        printf '%s\n' "$expected" | sed 's/^/    /'
        echo "  Got:"
        printf '%s\n' "$actual"  | sed 's/^/    /'
        FAIL=$((FAIL + 1))
    fi
}

check "basic_two_levels" \
    "$TESTS_DIR/logs/basic_two.log" \
    "LEVEL     COUNT  MOST RECENT
ERROR         1  disk full on /dev/sda1
INFO          2  request handled"

check "single_entry" \
    "$TESTS_DIR/logs/single.log" \
    "LEVEL     COUNT  MOST RECENT
ERROR         1  catastrophic failure in subsystem A"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
