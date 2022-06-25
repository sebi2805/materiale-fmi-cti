#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
 int upclin(char *numefis) {

 FILE *fp;

    fp = fopen(numefis,"r+");
    if(fp == NULL){
    puts("Open file failed\n");
    exit(-1);
    }

int maximumLineLength = 128;
    char *lineBuffer = (char *)malloc(sizeof(char) * maximumLineLength);

    if (lineBuffer == NULL) {
        printf("Eroare alocare memorie.");
        exit(1);
    }

    //char ch = getc(fp);
    int count = 0;

    

    while(fgets(lineBuffer, 128, fp)){


  
     
    lineBuffer[0]=lineBuffer[0]-32;
    fputs(lineBuffer , fp);
    if (count == maximumLineLength) {
            maximumLineLength += 128;
            lineBuffer = realloc(lineBuffer, maximumLineLength);
            if (lineBuffer == NULL) {
                printf("Eroare.");
                exit(1);
            }
        }
        
        count++;
    }
   
  
    free(lineBuffer);
    printf("Numarul de modificari:%d\n", count);
    return count;
}



int main(int argc, char *argv[]) {
  int k;
  if(argc != 2)
    {fprintf(stderr, "Utilizare: %s fisier\n", argv[0]); return 1;}
  if((k = upclin(argv[1])) == -1)
    {perror(argv[1]); return  1;}
  printf("%d\n", k);
  return 0;
}