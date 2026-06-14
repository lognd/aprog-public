#!/usr/bin/env bash
# Visible tests for cli-calculator.
# Compile: g++ -std=c++17 -o calc ../assets/main.cpp
# (after implementing): ./test_visible.sh ./calc

CALC="${1:-./calc}"
PASS=0
FAIL=0

check() {
    local desc="$1"; shift
    local expected="$1"; shift
    local got
    got="$("$CALC" "$@" 2>&1)"
    if [ "$got" = "$expected" ]; then
        PASS=$((PASS+1))
    else
        FAIL=$((FAIL+1))
        echo "FAIL: $desc"
        echo "  expected: $expected"
        echo "  got:      $got"
    fi
}

check "add"         "8"                          5 + 3
check "subtract"    "6"                          10 - 4
check "multiply"    "42"                         6 '*' 7
check "divide exact" "5"                         10 / 2
check "divide float" "3.5"                       7 / 2
check "modulo"      "1"                          10 '%' 3
check "no args"     "usage: calc <num1> <op> <num2>"
check "bad op"      "unknown operator: ^"        5 '^' 2
check "div by zero" "error: division by zero"    5 / 0

echo "$PASS check(s) passed"
[ "$FAIL" -gt 0 ] && echo "$FAIL check(s) FAILED" && exit 1 || exit 0
