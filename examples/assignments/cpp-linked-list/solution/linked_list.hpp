#pragma once
#include <cstddef>
#include <iostream>

template <typename T>
struct Node {
    T data;
    Node* next = nullptr;
    explicit Node(const T& value) : data(value) {}
};

template <typename T>
class LinkedList {
public:
    LinkedList() : head_(nullptr), tail_(nullptr), size_(0) {}

    LinkedList(const LinkedList& other) : head_(nullptr), tail_(nullptr), size_(0) {
        for (Node<T>* n = other.head_; n != nullptr; n = n->next)
            push_back(n->data);
    }

    ~LinkedList() {
        while (head_) {
            Node<T>* tmp = head_;
            head_ = head_->next;
            delete tmp;
        }
    }

    void push_back(const T& value) {
        Node<T>* n = new Node<T>(value);
        if (!tail_) { head_ = tail_ = n; }
        else         { tail_->next = n; tail_ = n; }
        ++size_;
    }

    void push_front(const T& value) {
        Node<T>* n = new Node<T>(value);
        n->next = head_;
        head_ = n;
        if (!tail_) tail_ = n;
        ++size_;
    }

    void pop_front() {
        if (!head_) return;
        Node<T>* tmp = head_;
        head_ = head_->next;
        if (!head_) tail_ = nullptr;
        delete tmp;
        --size_;
    }

    void pop_back() {
        if (!head_) return;
        if (head_ == tail_) { delete head_; head_ = tail_ = nullptr; --size_; return; }
        Node<T>* prev = head_;
        while (prev->next != tail_) prev = prev->next;
        delete tail_;
        tail_ = prev;
        tail_->next = nullptr;
        --size_;
    }

    T front() const { return head_->data; }
    T back()  const { return tail_->data; }

    std::size_t size()  const { return size_; }
    bool        empty() const { return size_ == 0; }

    void print() const {
        for (Node<T>* n = head_; n != nullptr; n = n->next) {
            if (n != head_) std::cout << ' ';
            std::cout << n->data;
        }
        std::cout << '\n';
    }

private:
    Node<T>* head_;
    Node<T>* tail_;
    std::size_t size_;
};
