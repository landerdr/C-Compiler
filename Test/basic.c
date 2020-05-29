
#include <stdio.h>

int f(int a) {
    //printf(a);
	if (a < 2 ) {
	    //printf("yay");
		return a;
	}
	else {
	    //printf(a);
		return f(a-1) + f(a-2);
		//return 2;
	}
}

// Recursive fibonnaci
int main(){
	int n;
    //printf("Enter a number:");
	scanf("%d",&n);
	int i = 1;
	while(i++ <= n){
	    //printf(i);
		printf("fib(%d)\t= %d;\n", i, f(i));
	}
	return 0;
}
