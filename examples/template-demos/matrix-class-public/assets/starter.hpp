// matrix-class.hpp -- class declaration. Do not modify this file.
#pragma once
#include <ostream>

class Matrix {
public:
    Matrix(int rows, int cols);
    Matrix(const Matrix &other);
    Matrix &operator=(const Matrix &other);
    ~Matrix();

    int rows() const;
    int cols() const;

    double &at(int r, int c);
    const double &at(int r, int c) const;

    Matrix operator+(const Matrix &rhs) const;
    Matrix operator*(const Matrix &rhs) const;
    Matrix transpose() const;

    void print(std::ostream &out) const;

private:
    int rows_;
    int cols_;
    double *data_;
};
