
int main(){
    float* i;
    float* c;
    float k = 5;
    int u = *c;
    c = &k;
    k += 1;
    *i += *c + k;
    //printf(*c);
    //printf(*i);
    return **i;

}

int f(){
    return 5;
}