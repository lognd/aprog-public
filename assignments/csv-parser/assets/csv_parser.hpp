#pragma once
#include <string>
#include <vector>

// Parse CSV text and return all rows as a vector of string vectors.
//
// Rules:
//   - Fields are separated by commas.
//   - Lines are separated by \n or \r\n.
//   - A field wrapped in " may contain commas and newlines.
//   - "" inside a quoted field represents a single literal ".
//   - An empty line produces a row with zero fields (do not skip it).
//   - A trailing comma produces an empty final field.
//   - Whitespace is NOT trimmed -- spaces are part of the field value.
//
// Implement this function in this file.  Do not change the signature.
std::vector<std::vector<std::string>> parse_csv(const std::string& text) {
    // TODO: implement
    (void)text;
    return {};
}
