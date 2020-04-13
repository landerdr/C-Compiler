#include <stdio.h>

int main() {

    char c = 'd';
    c %= c;
    c += 'e';
    c -= 1;
    c *= 1.1;
    c /= 1.1;
    printf(c); // excpecting c

    int i = 4;
    i += 4;
    i -= 2;
    i *= 10;
    i /= 4;
    i %= 6;
    printf(i); // excpecting 3

    float b = 5;
    b += 1;
    b -= 1;
    b *= 2;
    b /= 2;
    //b %= 3; // not allowed between floats
    printf(b); // excpecting 5.000000000

    return 0;
}