// cpp-bst.hpp -- implement all methods in this file.
// Do not add #include directives for STL containers.
#pragma once
#include <ostream>

class BST {
public:
    BST();
    ~BST();

    void insert(int value);
    bool search(int value) const;
    void inorder(std::ostream &out) const;

private:
    struct Node {
        int value;
        Node *left;
        Node *right;
        Node(int v) : value(v), left(nullptr), right(nullptr) {}
    };

    Node *root_;

    // TODO: declare any private helper methods you need.
};
