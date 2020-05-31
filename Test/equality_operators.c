#include <stdio.h>

int main() {

    char c = 'd';
    c %= c;
    c += 'e';
    c -= 1;
    c *= 1.1;
    int j = c;
    c /= 1.1;
    printf("%c;", c); // expecting d

    int i = 4;
    i += 4;
    i -= 2;
    i *= 10;
    i /= 4;
    i %= 6;
    //printf("%d;",i); // expecting 3

    float b = 5;
    b += 1;
    b -= 1;
    b *= 2;
    b /= 2;
    //b %= 3; // not allowed between floats
    //printf("%f;",b); // expecting 5.000000000

    return 0;
}