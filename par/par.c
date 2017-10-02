#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    unsigned int P[0xFFFF+1]={0,};
    int i,j;
    unsigned short k=0;
    unsigned short N=0;  //16비트, 2바이트

    int inum;
    unsigned point=0;
    unsigned bpoint=0;
    char line[1024];
	printf ("argc %d \n", argc);
	return 0;
    if (argc >=1) freopen(argv[1], "r", stdin);

    while(fgets(line, 1024, stdin)) {
	point = atoi(line);   
	//printf("%d \n", point);

    //for(i=0; i< 0xFFFFF; i++){
        //if(1&rand()) N=N|1;
        //else N=N|0;
	if (point>bpoint) N=N|1; else N=N|0;
	bpoint = point;
        P[N]++;
        k=0x8000; //1000 0000 0000 0000
        //for(j=1;j<=8;j++){
        //        if(N&k) printf("1");
        //        else printf("0");
        //        k=k >> 1;
        //}
        //printf("\n");
        N = N << 1;
    }
    for(i=0; i< 0xFFFF; i++){
	if(P[i] ==0) continue;
	k=0x8000;
	for(j=1;j<=16;j++){
		if(i&k) printf("1");
		else printf("0");
		k=k >> 1;
	}
        printf(" %d \n", P[i]);
    }
    return 1;
}

