#include <iostream>
#include <string>

// BUG 1: missing base case -- will recurse forever on n >= 10
int digit_sum(int n) {
    // TODO: add base case: if (n < 10) return n;
    return (n % 10) + digit_sum(n / 10);
}

// BUG 2: wrong recursive step -- swaps wrong characters
std::string reverse_str(const std::string& s, int i, int j) {
    if (i >= j) return s;
    std::string t = s;
    std::swap(t[i], t[j + 1]);  // BUG: should be t[j], not t[j+1]
    return reverse_str(t, i + 1, j - 1);
}

int main() {
    std::cout << digit_sum(493) << "\n";
    std::cout << reverse_str("hello", 0, 4) << "\n";
}
