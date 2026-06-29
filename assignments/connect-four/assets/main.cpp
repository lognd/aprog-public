#include <cstdio>
#include <cstdlib>
#include <cstring>
#include "board.hpp"
#include "grid.hpp"

static const int ROWS = 6;
static const int COLS = 7;

// Print the board followed by a blank line.
// Cells are separated by spaces; column numbers appear on the bottom row.
static void print_board(const char* board) {
    for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLS; ++c) {
            if (c > 0) printf(" ");
            printf("%c", cell_at(board, COLS, r, c));
        }
        printf("\n");
    }
    for (int c = 0; c < COLS; ++c) {
        if (c > 0) printf(" ");
        printf("%d", c);
    }
    printf("\n\n");
}

// Prompt for a column number. Re-prompts on invalid input or full column.
static int read_column(const char* board, const char* prompt) {
    char line[64];
    while (true) {
        printf("%s", prompt);
        fflush(stdout);
        if (!fgets(line, sizeof(line), stdin)) return -1;
        char* end;
        long col = strtol(line, &end, 10);
        if (end == line || col < 0 || col >= COLS) {
            printf("Invalid column. Enter 0-%d.\n", COLS - 1);
            continue;
        }
        if (!cell_is(board, COLS, 0, (int)col, '.')) {
            printf("Column %ld is full. Try again.\n", col);
            continue;
        }
        return (int)col;
    }
}

static void run_two_player(char* board) {
    const char pieces[2] = {'X', 'O'};
    int turn = 0;
    while (true) {
        print_board(board);
        char prompt[32];
        snprintf(prompt, sizeof(prompt), "Player %c's turn (0-6): ", pieces[turn]);
        int col = read_column(board, prompt);
        if (col < 0) return;
        drop_piece(board, ROWS, COLS, col, pieces[turn]);
        if (check_win(board, ROWS, COLS, pieces[turn])) {
            print_board(board);
            printf("Player %c wins!\n", pieces[turn]);
            return;
        }
        if (is_full(board, ROWS, COLS)) {
            print_board(board);
            printf("It's a draw!\n");
            return;
        }
        turn = 1 - turn;
    }
}

static void run_vs_computer(char* board) {
    while (true) {
        print_board(board);
        int col = read_column(board, "Your turn (0-6): ");
        if (col < 0) return;
        drop_piece(board, ROWS, COLS, col, 'X');
        if (check_win(board, ROWS, COLS, 'X')) {
            print_board(board);
            printf("Player X wins!\n");
            return;
        }
        if (is_full(board, ROWS, COLS)) {
            print_board(board);
            printf("It's a draw!\n");
            return;
        }
        int ai_col = computer_move(board, ROWS, COLS, 'O', 'X');
        drop_piece(board, ROWS, COLS, ai_col, 'O');
        printf("Computer plays column %d.\n", ai_col);
        if (check_win(board, ROWS, COLS, 'O')) {
            print_board(board);
            printf("Player O wins!\n");
            return;
        }
        if (is_full(board, ROWS, COLS)) {
            print_board(board);
            printf("It's a draw!\n");
            return;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s --two-player | --vs-computer\n", argv[0]);
        return 1;
    }

    char board[ROWS * COLS];
    fill_grid(board, ROWS, COLS, '.');

    if (strcmp(argv[1], "--two-player") == 0) {
        run_two_player(board);
    } else if (strcmp(argv[1], "--vs-computer") == 0) {
        run_vs_computer(board);
    } else {
        fprintf(stderr, "Unknown mode: %s\n", argv[1]);
        return 1;
    }
    return 0;
}
