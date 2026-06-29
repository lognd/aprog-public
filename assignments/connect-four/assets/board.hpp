#pragma once

// Connect Four board logic.
// The board is a flat char array in row-major order (rows x cols).
// Empty cells are '.', player 1 is 'X', player 2 / computer is 'O'.

// Drop piece into the lowest empty row of the given column.
// Returns true on success, false if the column is full.
bool drop_piece(char* board, int rows, int cols, int column, char piece);

// Return true if piece has four in a row (horizontal, vertical,
// or either diagonal direction).
bool check_win(const char* board, int rows, int cols, char piece);

// Return true if every cell is non-'.'.
bool is_full(const char* board, int rows, int cols);

// Return the column the computer should play.
// Priority:
//   1. Win immediately if possible.
//   2. Block the opponent from winning next turn.
//   3. Play the non-full column closest to center (cols/2).
//      Among columns equally close to center, prefer the lower-indexed one.
int computer_move(const char* board, int rows, int cols,
                  char computer_piece, char human_piece);
