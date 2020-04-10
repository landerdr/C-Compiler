
#include <stdio.h>

int main(){

    //int i[3];
    int j[3];
    int i = 0;
    j[i] = 1;
    j[i]++;
    j[i] *= 2;
    j[i] = j[0] - 3;
    printf("%d\n", j[0]);

    int k[6] = {0, 1, 2};
    printf("%d\n", k[2]);

    int z = 10;
    float r[] = {0, 1, 2+z};
    printf("%f\n", r[2]);

    char c[] = {'a', 'b', 'c'};
    printf("%c\n", c[2]);

    return 0;
}