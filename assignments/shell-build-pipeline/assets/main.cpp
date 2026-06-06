#include <iostream>
#include "greet.h"
#include "math_utils.h"

int main() {
    std::cout << greet("world") << "\n";
    int result = add(multiply(6, 7), 0);
    std::cout << "answer: " << result << "\n";
    if (result == 42) {
        std::cout << "passphrase: STAGES_COMPLETE\n";
    }
    return 0;
}
