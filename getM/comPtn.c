#include <stdio.h>
#include <stdlib.h>

static unsigned short PT[0xFFFF + 1] = { 0, };
static unsigned short N = 0;

int main(int argc, char *argv[]) {
	int i = 0,j = 0;
	char line[1024];
	FILE *pFile;
	
	int spc = 0, epc = 0, lpc = 0, hpc = 0, trc = 0;
	int spb = 0, epb = 0, lpb = 0, hpb = 0, trb = 0;
	unsigned int ptn;
	unsigned int cnt;
	pFile = fopen("Pattern.dat", "r");
	if (pFile != NULL) {
		while ((pFile != NULL) && !feof(pFile)) {
			fscanf(pFile, "%d %d", &ptn, &cnt);
			PT[ptn] = cnt;
		}
		fclose(pFile);
	}
	switch (argc) {
	case 1: 
		printf("Usage : for i in [0-9]*.data; do ./comPtn $i; done\n");
		return 0;
	        pFile = fopen("data.txt", "w");
        	for (i = 0; i < 0xFFFF; i++) {
                	sprintf(line, "2010.01.01 %d %d %d %d %d \n", rand() % 999, rand() % 999, rand() % 999, rand() % 999, rand() % 999);
                	fprintf(pFile, "%s", line);
       		}
        	fclose(pFile);
		pFile = fopen("data.txt", "r");		
		printf("Usage : for i in [0-9]*.data; do ./comPtn $i  done\n");
		break;
	case 2:
		pFile = fopen(argv[1], "r");		
		printf("working file : [%s] \n", argv[1]);
		break;

	default:
		printf("Usage : for i in [0-9]*.data; do ./comPtn $i  done\n");
		return 0;
		break;
	}	
	if (pFile == NULL) {
		printf("fail to open data file:[%s] \n", argv[1]);
		return 0;
	}
	int cnt16=0;
	while (!feof(pFile)) {
		fscanf(pFile, "%s %d %d %d %d %d", line, &epc, &spc,  &hpc, &lpc, &trc);
		//spc = rand() % 100;
		//spb = rand() % 100;
		if (spc==spb) continue;
		N = N << 1;    //c
		if (spc > spb)   //전일자 대비 상승했으면 
			N = N | 1; //1로 설정
		else
			N = N | 0;
		if (cnt16 < 16) cnt16 +=1;
		else PT[N] += 1;
		epb = epc; spb = spc; lpb = lpc; hpb = hpc; trb = trc;

		//printf("%b \n", N);
		unsigned k = 0x8000; //1000 0000 0000 0000
		/*
		for(j=1;j<=16;j++){
		  if(N&k) printf("1");
		  else printf("0");
		  k=k >> 1;
		}
		printf("\n");
		*/
	}
	/*
	for (i = 0; i < 0xFFFF; i++) {
		printf("%d \n", PT[i]);
	}
	*/

	pFile = fopen("Pattern.dat", "w");
	for (i = 0; i <= 0xFFFF; i++) {
		fprintf(pFile, "%d %d\n", i, PT[i]);
	}
	fclose(pFile);
	return 1;
}
