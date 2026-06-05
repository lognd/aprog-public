// Visible test driver — compile with: g++ -std=c++17 -o collatz_test test_collatz.cpp -I..
// Calls collatz() with a small input so students can verify their implementation locally.

#include "../assets/collatz.hpp"

int main() {
    collatz(5);
    return 0;
}
