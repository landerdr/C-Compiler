#include <stdio.h>

int main()
{
    int a = 5;
    int b = 5;
    int c = a + b;
    b = c + a;
    c = c - b;
    int x = -c;
    x -= x;
    int d = 2;
    a = c - 4 + -1;
    int i = 1 < 0;
    a++;
    int r = 0;
    int s = r += 5;
    int u = 3;
    u = u*1.0;
    int k = u && 0;
    k = u || 0;

    return 0;
}