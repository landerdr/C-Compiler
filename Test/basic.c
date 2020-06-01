#include <stdio.h>
// Should print the numbers 1 2 3

int main(){

    char c = 'c';
    char j[] = {'c', 'b', 'c', 'd'};
    j[2] = 'f';
    printf("%c", j[2]);

    return 0;
}
