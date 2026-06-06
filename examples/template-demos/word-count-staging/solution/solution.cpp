// Reference solution for Word Count.
#include <iostream>
#include <sstream>
#include <string>

int main() {
    std::string line;
    int line_num = 0;
    int total = 0;
    while (std::getline(std::cin, line)) {
        ++line_num;
        std::istringstream iss(line);
        std::string word;
        int count = 0;
        while (iss >> word) ++count;
        total += count;
        if (count == 1)
            std::cout << "Line " << line_num << ": 1 word\n";
        else
            std::cout << "Line " << line_num << ": " << count << " words\n";
    }
    if (total == 1)
        std::cout << "Total: 1 word\n";
    else
        std::cout << "Total: " << total << " words\n";
    return 0;
}
