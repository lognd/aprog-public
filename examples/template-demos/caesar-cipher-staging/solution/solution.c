/* Reference solution for Caesar Cipher. */
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int shift = ((atoi(argv[1]) % 26) + 26) % 26;
    int c;
    while ((c = getchar()) != EOF) {
        if (c >= 'a' && c <= 'z')
            c = (c - 'a' + shift) % 26 + 'a';
        else if (c >= 'A' && c <= 'Z')
            c = (c - 'A' + shift) % 26 + 'A';
        putchar(c);
    }
    return 0;
}
