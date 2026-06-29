#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>

// TODO: implement log-analyzer
//
// Usage: ./log-analyzer <logfile>
//
// Read the log file line by line.  Each line has the form:
//   TIMESTAMP LEVEL MESSAGE...
//
// Track the count and most recent message for each level.
// Print a formatted summary table to stdout (see README.md).
//
// If the file cannot be opened, print to stderr and exit 1:
//   error: cannot open <logfile>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "usage: log-analyzer <logfile>\n";
        return 1;
    }

    // TODO: open argv[1] with std::ifstream and check is_open()

    // TODO: read line by line with std::getline
    //       for each line, use std::istringstream to extract ts, level, message
    //       track counts and most-recent message per level
    //       count malformed lines (fewer than 2 tokens)

    // TODO: print the header and one row per level (alphabetical order)
    //       use std::left/std::right and std::setw for alignment

    // TODO: if malformed > 0, print "N malformed line(s) skipped"

    return 0;
}
