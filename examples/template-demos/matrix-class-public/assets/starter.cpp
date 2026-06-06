// matrix-class.cpp -- implement all methods declared in matrix-class.hpp.
#include "matrix-class.hpp"

Matrix::Matrix(int rows, int cols) : rows_(rows), cols_(cols), data_(nullptr) {
    // TODO: allocate data_ and zero-initialize
}

Matrix::Matrix(const Matrix &other) : rows_(other.rows_), cols_(other.cols_), data_(nullptr) {
    // TODO: deep copy
}

Matrix &Matrix::operator=(const Matrix &other) {
    // TODO: copy-assignment (handle self-assignment)
    return *this;
}

Matrix::~Matrix() {
    // TODO: free data_
}

int Matrix::rows() const { return rows_; }
int Matrix::cols() const { return cols_; }

double &Matrix::at(int r, int c) {
    // TODO: return reference to element at (r, c)
    return data_[0]; // placeholder
}

const double &Matrix::at(int r, int c) const {
    // TODO
    return data_[0]; // placeholder
}

Matrix Matrix::operator+(const Matrix &rhs) const {
    // TODO
    return Matrix(rows_, cols_);
}

Matrix Matrix::operator*(const Matrix &rhs) const {
    // TODO: rows_ x rhs.cols_ result
    return Matrix(rows_, rhs.cols_);
}

Matrix Matrix::transpose() const {
    // TODO: cols_ x rows_ result
    return Matrix(cols_, rows_);
}

void Matrix::print(std::ostream &out) const {
    // TODO: print rows, each on its own line, values space-separated
}
