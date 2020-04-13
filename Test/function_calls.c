
#include <stdio.h>

int f1(){
    printf(1);
    return 1;
}

int f2(int i){
    printf(i);
    return 1;
}


int f3(int i, float j){
    return i + j;
}

void f4(){
    printf(4);
    return;
}

float f5(){
    return 0.5;
}

char* f6(char* a){
    return a;
}

char f7(char a){
    return a;
}


int f8(int a[3]){
    return a[2];
}

int main(){

    f1();
    f2(2);
    printf(f3(1, 2.0));
    f4();
    printf(f5());
    printf(f6("abc"));
    printf(f7('a'));

    int a[4] = {0, 1, 2};
    printf("%d", f8(a));

    return 0;
}

