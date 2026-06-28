#pragma once

// Returns n + 1.
// This is the only function where a +1 increment is allowed.
int successor(int n);

// Returns a + b.
// Implement using only successor() and recursion.  No + operator.
int add(int a, int b);

// Returns a * b.
// Implement using only add() and recursion.  No * operator.
int multiply(int a, int b);

// Returns base raised to the power exp.
// base^0 == 1 for all base.
// Implement using only multiply() and recursion.
int exponentiate(int base, int exp);
