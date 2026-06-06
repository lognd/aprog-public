// CLI driver for BST.
//
// Compiled twice:
//   "cpp-bst"   -- includes student's header (from grader/ after injection)
//   "reference" -- includes staff solution (from hidden-tests/)
//
// Commands (from argv):
//   insert <n>   -- insert integer n
//   search <n>   -- print "found" or "not found"
//   inorder      -- print inorder traversal

#include <iostream>
#include <string>
#include "cpp-bst.hpp"

int main(int argc, char *argv[]) {
    BST t;
    for (int i = 1; i < argc; ++i) {
        std::string cmd = argv[i];
        if (cmd == "insert") {
            t.insert(std::stoi(argv[++i]));
        } else if (cmd == "search") {
            std::cout << (t.search(std::stoi(argv[++i])) ? "found" : "not found") << "\n";
        } else if (cmd == "inorder") {
            t.inorder(std::cout);
        }
    }
    return 0;
}
