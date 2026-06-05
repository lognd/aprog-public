// Grader-owned driver for the oracle / differential / valgrind test steps.
//
// The student header (linked_list.hpp) is included from the submission
// directory, which is passed as -I<submission> at compile time.
//
// Command-line interface used by the grader:
//
//   ./linked_list <command> [<command> ...]
//
// Each command is executed in sequence.  Supported commands:
//
//   push_back <value>    --  push_back(value)
//   push_front <value>   --  push_front(value)
//   pop_front            --  pop_front()
//   pop_back             --  pop_back()
//   front                --  print front() on a line
//   back                 --  print back() on a line
//   size                 --  print "size=N\n"
//   print                --  call print()
//   copy_push <value>    --  deep-copy the list, push_back(value) to the copy,
//                         print the original, then print the copy (tests
//                         that the original is untouched)

#include <cstdlib>
#include <iostream>
#include <string>
#include "linked_list.hpp"

int main(int argc, char* argv[]) {
    LinkedList<int> lst;
    int i = 1;
    while (i < argc) {
        std::string cmd = argv[i++];
        if (cmd == "push_back" && i < argc) {
            lst.push_back(std::atoi(argv[i++]));
        } else if (cmd == "push_front" && i < argc) {
            lst.push_front(std::atoi(argv[i++]));
        } else if (cmd == "pop_front") {
            lst.pop_front();
        } else if (cmd == "pop_back") {
            lst.pop_back();
        } else if (cmd == "front") {
            std::cout << "front=" << lst.front() << "\n";
        } else if (cmd == "back") {
            std::cout << "back=" << lst.back() << "\n";
        } else if (cmd == "size") {
            std::cout << "size=" << lst.size() << "\n";
        } else if (cmd == "print") {
            lst.print();
        } else if (cmd == "copy_push" && i < argc) {
            LinkedList<int> copy = lst;
            copy.push_back(std::atoi(argv[i++]));
            lst.print();
            copy.print();
        }
    }
    return 0;
}
