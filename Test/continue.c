
#include <stdio.h>

int main(){

    int j = 0;
    while(j < 4){

        if (j == 2){
            j ++;
            continue;
        }

        printf("%d", j);
        j ++;
    }

    j = 0;
    do{
        if (j == 2){
            j ++;
            continue;
        }

        printf("%d", j);
        j ++;
     }while(j < 4);



    for (int i = 0; i < 4; i ++){

        if (i == 2){
            continue;
        }

        printf("%d", i);

    }

    return 0;

}