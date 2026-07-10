#include <iostream>
#include <string>
#include <ctime>
#include "tga.hpp"
#include "operations.hpp"

static std::string get_season() {
    std::time_t t = std::time(nullptr);
    std::tm* now = std::localtime(&t);
    int month = now->tm_mon + 1;  // tm_mon is 0-indexed
    if (month <= 4) return "Spring";
    if (month <= 8) return "Summer";
    return "Fall";
}

static int get_year() {
    std::time_t t = std::time(nullptr);
    std::tm* now = std::localtime(&t);
    return now->tm_year + 1900;
}

static void print_help() {
    std::cout << "Project 1: Image Processing, "
              << get_season() << " " << get_year() << "\n\n"
              << "Usage:\n"
              << "\t./project1.out [output] [firstImage] [method] [...]\n";
}

static bool ends_with_tga(const std::string& s) {
    if (s.size() < 4) return false;
    return s.substr(s.size() - 4) == ".tga";
}

static bool file_exists(const std::string& path) {
    std::ifstream f(path, std::ios::binary);
    return f.good();
}

static bool is_number(const std::string& s) {
    // TODO: return true if s represents a valid integer or float
    // Allow leading '-' for negatives
    return false;
}

int main(int argc, char* argv[]) {
    // TODO: verify the host is little-endian before doing anything else.
    // Store a uint16_t holding 1, inspect its first byte through an
    // unsigned char pointer, and compare it to 1. If the host is
    // big-endian, print "error: big-endian host unsupported" to
    // std::cerr and return 1 immediately. See the Background section of
    // the README for why this matters and exactly how to write the check.

    if (argc < 2 || std::string(argv[1]) == "--help") {
        print_help();
        return 0;
    }

    // TODO: validate output filename (argv[1]) -- must end in .tga
    // TODO: validate input filename (argv[2]) -- must end in .tga and exist
    // TODO: load the input image
    // TODO: loop through remaining arguments, dispatch to operations
    // TODO: write output image

    std::cerr << "Not yet implemented.\n";
    return 1;
}
