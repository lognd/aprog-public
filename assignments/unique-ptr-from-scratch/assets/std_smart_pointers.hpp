// Part 2 -- using std::unique_ptr instead of building your own.
//
// Shape, Circle, and Square are complete -- do not modify them. Implement
// the three functions below using std::unique_ptr and std::make_unique.
//
// Rules:
//   - Do not use `new` or `delete` directly -- use std::make_unique.
//   - Do not use exceptions (throw/try/catch) anywhere in this file.
//   - Do not modify the function signatures below.
#pragma once

#include <memory>
#include <string>
#include <vector>

// Abstract shape interface. Complete -- do not modify.
class Shape {
public:
    virtual ~Shape() = default;
    virtual double area() const = 0;
};

// Complete -- do not modify.
class Circle : public Shape {
public:
    explicit Circle(double radius) : radius_(radius) {}
    double area() const override { return 3.14159265358979 * radius_ * radius_; }

private:
    double radius_;
};

// Complete -- do not modify.
class Square : public Shape {
public:
    explicit Square(double side) : side_(side) {}
    double area() const override { return side_ * side_; }

private:
    double side_;
};

// Factory function: builds a shape by name and returns ownership of it.
//   kind == "circle" -> a Circle with radius = size
//   kind == "square" -> a Square with side = size
//   anything else    -> return an empty (null) std::unique_ptr<Shape>
//
// Use std::make_unique<Circle>(...) / std::make_unique<Square>(...) --
// do not call `new` directly.
inline std::unique_ptr<Shape> make_shape(const std::string& kind, double size) {
    // TODO
    (void)kind;
    (void)size;
    return nullptr;
}

// Takes the vector by reference -- this function only inspects the shapes,
// it must not take ownership of any of them and must not shrink or grow
// the vector. Returns the sum of area() over every non-null entry. A null
// entry (a moved-from unique_ptr) contributes 0.
inline double total_area(const std::vector<std::unique_ptr<Shape>>& shapes) {
    // TODO
    (void)shapes;
    return 0.0;
}

// Finds the shape with the largest area() in shapes, moves it out of the
// vector (the vector's slot at that index becomes an empty/null
// unique_ptr -- do not erase the element, just leave it null), and returns
// it by value to the caller. If shapes is empty or every entry is already
// null, returns an empty std::unique_ptr<Shape>.
//
// Calling this correctly requires std::move: you cannot copy a
// std::unique_ptr out of the vector, only move it.
inline std::unique_ptr<Shape> claim_biggest(std::vector<std::unique_ptr<Shape>>& shapes) {
    // TODO
    (void)shapes;
    return nullptr;
}
