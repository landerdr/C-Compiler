
int main() {

    for (int i = 0; i < 8; i ++){
        if (i == 2){
            continue;
        }
        if (i == 5){
            break;
        }
        printf(i);
    }

    return 0;

}