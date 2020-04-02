

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

char f6(){
    return 'a';
}

int main(){

    f1();
    f2(2);
    printf(f3(1, 2.0));
    f4();
    printf(f5());
    printf(f6());

    return 0;
}

