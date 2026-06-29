#include "board.hpp"
#include "grid.hpp"

bool drop_piece(char* board, int rows, int cols, int column, char piece) {
    // TODO: find the lowest empty row in the given column and place piece there.
    // Return false if the column is full (top cell is not '.').
    return false;
}

bool check_win(const char* board, int rows, int cols, char piece) {
    // TODO: check all four directions for four in a row.
    // Directions: horizontal, vertical, diagonal (top-left to bottom-right),
    // anti-diagonal (top-right to bottom-left).
    return false;
}

bool is_full(const char* board, int rows, int cols) {
    // TODO: return true if no cell equals '.'.
    return false;
}

int computer_move(const char* board, int rows, int cols,
                  char computer_piece, char human_piece) {
    // TODO: implement the three-priority strategy described in board.hpp.
    return 0;
}
