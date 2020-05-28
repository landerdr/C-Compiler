
void f(){

    int i = 4;

    int* j = &i;
    *j = 2;
    printf(*j);

}



int main() {

    f();
    f();

    return 0;

}