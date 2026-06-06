// Reference solution for Reverse String.
#include <algorithm>
#include <iostream>
#include <string>

int main() {
    std::string line;
    std::getline(std::cin, line);
    std::reverse(line.begin(), line.end());
    std::cout << line << "\n";
    return 0;
}
