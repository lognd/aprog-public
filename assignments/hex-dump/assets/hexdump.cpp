// hexdump.cpp
//
// Usage: ./hexdump <filename>
//
// Print the contents of <filename> in xxd -g 1 format:
//
//   00000000: 48 65 6c 6c 6f 2c 20 77 6f 72 6c 64 0a 00 00 00  Hello, world....
//
// Format details:
//   - Offset:    8 hex digits, lowercase, followed by a colon and a space
//   - Hex block: up to 16 bytes, each as 2 hex digits separated by spaces,
//                padded with spaces if the line has fewer than 16 bytes
//   - Separator: two spaces between the hex block and the ASCII block
//   - ASCII:     printable bytes as-is; non-printable bytes as '.'
//
// Rules:
//   - Use only: open(), read(), write(), close(), exit()
//   - No printf, fprintf, sprintf, snprintf, cout, fopen, or malloc
//   - All output goes through write()
//   - Use stack-allocated buffers only

#include <fcntl.h>   // open(), O_RDONLY
#include <unistd.h>  // read(), write(), close()
#include <stdio.h>   // perror()

// Bytes per line in the output.
static const int COLS = 16;

// ---------------------------------------------------------------------------
// Helper: write a single byte to fd as a 2-digit lowercase hex string.
// ---------------------------------------------------------------------------
static void write_hex_byte(int fd, unsigned char b) {
    // TODO
}

// ---------------------------------------------------------------------------
// Helper: write a 32-bit unsigned integer to fd as exactly 8 lowercase hex
// digits (with leading zeros).
// ---------------------------------------------------------------------------
static void write_hex32(int fd, unsigned int n) {
    // TODO
}

// ---------------------------------------------------------------------------
// Helper: write a single byte to fd as a printable ASCII character, or '.'
// if the byte is not printable (< 0x20 or >= 0x7f).
// ---------------------------------------------------------------------------
static void write_ascii_byte(int fd, unsigned char b) {
    // TODO
}

// ---------------------------------------------------------------------------
// format_line: format and write one output line.
//
//   offset -- byte offset of the first byte on this line
//   buf    -- the raw bytes for this line
//   n      -- number of bytes in buf (1..COLS)
// ---------------------------------------------------------------------------
static void format_line(int fd, unsigned int offset, const unsigned char *buf, int n) {
    // TODO:
    //   1. Write the offset as 8 hex digits, then ": "
    //   2. Write each byte as "XX ", padding missing columns with "   "
    //   3. Write two spaces
    //   4. Write each byte as a printable character or '.'
    //   5. Write a newline '\n'
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        write(2, "usage: hexdump <file>\n", 21);
        exit(1);
    }

    // TODO: open argv[1] for reading; on failure perror() and exit(1)

    unsigned char buf[COLS];
    unsigned int  offset = 0;
    ssize_t       n;

    // TODO: read loop -- call read(), then format_line(), advance offset

    // TODO: close the fd

    return 0;
}
