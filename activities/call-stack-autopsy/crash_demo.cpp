#include <iostream>
#include <string>

// Simulates a tiny expression evaluator that stack-overflows
// on unbalanced input.

int eval(const std::string& expr, int pos);

int parse_number(const std::string& expr, int pos) {
    if (pos >= (int)expr.size()) {
        // Bug: should have validated earlier. Infinite recursion path here.
        return eval(expr, pos);
    }
    int val = 0;
    while (pos < (int)expr.size() && expr[pos] >= '0' && expr[pos] <= '9') {
        val = val * 10 + (expr[pos] - '0');
        ++pos;
    }
    return val;
}

int eval(const std::string& expr, int pos) {
    return parse_number(expr, pos);
}

int main() {
    std::string input = "";   // empty input triggers the bug
    std::cout << eval(input, 0) << std::endl;
    return 0;
}
