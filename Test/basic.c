#include <stdio.h>
// Should print the numbers 1 2 3

int m[4] = {1, 2, 3, 4};
char ma[] = {'a', 'b', 'c', 'd'};
int mb[4];

float f[4] = {0.1, 0.2, 3.0, 4.0};

int main(){

   // printf(m[1]);
   // printf(ma[2]);
    ma[2] = 99;
    printf(ma[1]);
    printf(ma[2]);
    printf(ma[3]);

    char a = 99;
    char b = 99;
    printf(a);
    printf(b);
    printf(f[2]);

   // printf(mb[3]);
   // printf(ma);
    return 0;
}
