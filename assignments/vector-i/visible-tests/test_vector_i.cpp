// Visible smoke test -- compile: g++ -std=c++17 -Wall -Wextra -o test_vi test_vector_i.cpp -I../assets
// A clean compile with no warnings is a good first indicator your fixes are correct.

#include "../assets/vector_i.hpp"
#include <iostream>

int main() {
    VectorI v;
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);

    VectorI v2 = v;       // copy constructor
    VectorI v3 = std::move(v);  // move constructor

    std::cout << "ok" << std::endl;
    return 0;
}
