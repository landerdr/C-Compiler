#include <stdio.h>

int x = 123;
int* y = &x;

char x1 = 123;
char* y1 = &x1;
char* z1 = "bla bla bla";

float x2 = 123;
float* y2 = &x2;

int main(){

    printf(x);
    printf(*y);

    printf(x1);
    printf(*y1);
    printf(z1);

    printf(x2);
    printf(*y2);

    return 0;

}