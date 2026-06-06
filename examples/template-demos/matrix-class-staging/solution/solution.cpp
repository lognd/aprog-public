// matrix-class.cpp -- reference solution implementation.
#include "matrix-class.hpp"
#include <cstring>
#include <stdexcept>

Matrix::Matrix(int rows, int cols)
    : rows_(rows), cols_(cols), data_(new double[rows * cols]()) {}

Matrix::Matrix(const Matrix &other)
    : rows_(other.rows_), cols_(other.cols_), data_(new double[other.rows_ * other.cols_]) {
    std::memcpy(data_, other.data_, rows_ * cols_ * sizeof(double));
}

Matrix &Matrix::operator=(const Matrix &other) {
    if (this == &other) return *this;
    delete[] data_;
    rows_ = other.rows_;
    cols_ = other.cols_;
    data_ = new double[rows_ * cols_];
    std::memcpy(data_, other.data_, rows_ * cols_ * sizeof(double));
    return *this;
}

Matrix::~Matrix() { delete[] data_; }

int Matrix::rows() const { return rows_; }
int Matrix::cols() const { return cols_; }

double &Matrix::at(int r, int c) { return data_[r * cols_ + c]; }
const double &Matrix::at(int r, int c) const { return data_[r * cols_ + c]; }

Matrix Matrix::operator+(const Matrix &rhs) const {
    Matrix result(rows_, cols_);
    for (int i = 0; i < rows_ * cols_; ++i)
        result.data_[i] = data_[i] + rhs.data_[i];
    return result;
}

Matrix Matrix::operator*(const Matrix &rhs) const {
    Matrix result(rows_, rhs.cols_);
    for (int i = 0; i < rows_; ++i)
        for (int j = 0; j < rhs.cols_; ++j)
            for (int k = 0; k < cols_; ++k)
                result.at(i, j) += at(i, k) * rhs.at(k, j);
    return result;
}

Matrix Matrix::transpose() const {
    Matrix result(cols_, rows_);
    for (int i = 0; i < rows_; ++i)
        for (int j = 0; j < cols_; ++j)
            result.at(j, i) = at(i, j);
    return result;
}

void Matrix::print(std::ostream &out) const {
    for (int i = 0; i < rows_; ++i) {
        for (int j = 0; j < cols_; ++j) {
            if (j > 0) out << " ";
            out << at(i, j);
        }
        out << "\n";
    }
}
