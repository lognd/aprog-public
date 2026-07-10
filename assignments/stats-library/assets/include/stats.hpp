#pragma once
#include <vector>
#include <limits>

namespace stats {

// Returns the arithmetic mean of data.
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double mean(const std::vector<double>& data);

// Returns the median of data.
// Takes data by value and sorts it internally.
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double median(std::vector<double> data);

// Returns all modes (values with the highest frequency) sorted in ascending order.
// If every value appears once, every value is a mode.
// Returns an empty vector if data is empty.
std::vector<double> mode(const std::vector<double>& data);

// Returns the population variance of data (mean of squared deviations from the mean).
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double variance(const std::vector<double>& data);

// Returns the population standard deviation of data (square root of variance).
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double stddev(const std::vector<double>& data);

// Returns the minimum value in data.
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double minimum(const std::vector<double>& data);

// Returns the maximum value in data.
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double maximum(const std::vector<double>& data);

// Returns maximum(data) - minimum(data).
// Returns std::numeric_limits<double>::quiet_NaN() if data is empty.
double range(const std::vector<double>& data);

}  // namespace stats
