// Reference solution for cpp-bst.hpp.
#pragma once
#include <ostream>

class BST {
public:
    BST() : root_(nullptr) {}

    ~BST() { destroy(root_); }

    void insert(int value) { root_ = insert(root_, value); }

    bool search(int value) const {
        Node *n = root_;
        while (n) {
            if (value == n->value) return true;
            n = value < n->value ? n->left : n->right;
        }
        return false;
    }

    void inorder(std::ostream &out) const {
        bool first = true;
        inorder(root_, out, first);
        out << "\n";
    }

private:
    struct Node {
        int value;
        Node *left;
        Node *right;
        Node(int v) : value(v), left(nullptr), right(nullptr) {}
    };

    Node *root_;

    Node *insert(Node *n, int value) {
        if (!n) return new Node(value);
        if (value < n->value) n->left = insert(n->left, value);
        else if (value > n->value) n->right = insert(n->right, value);
        return n;
    }

    void inorder(Node *n, std::ostream &out, bool &first) const {
        if (!n) return;
        inorder(n->left, out, first);
        if (!first) out << " ";
        out << n->value;
        first = false;
        inorder(n->right, out, first);
    }

    void destroy(Node *n) {
        if (!n) return;
        destroy(n->left);
        destroy(n->right);
        delete n;
    }
};
