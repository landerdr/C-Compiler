
int main(){
    int* i;
    int* c;
    int k = 5;
    int k2 = 5;
    i = &k2;
    c = &k;
    *i = 0;
    *c = 0;
    *c = k--;
    *i = --k2;

    printf(*c);
    printf(*i);
    printf(k);
    printf(k2);

    return k;

}

int f(){
    return 5;
}