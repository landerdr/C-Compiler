#include <stdio.h>

int main(){

    int * a;
    int b = 0;
    a = &b;
    *a = 5;
    int c = *a;

    printf(*a);
    printf(b);
    printf(c);

    printf(a);
    printf(&b);
    printf(&c);

    return 0;

}