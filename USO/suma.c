
include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
int main(int argc, char *argv[]) {
 int d[2], n, s;
 printf("Suma lui Gauss 1 + ... + %d = ", atoi(argv[1]));
 pipe(d);
 for(n=1; n <= atoi(argv[1]); ++n)
   if(!fork())
     {dup2(d[1],1); close(d[0]); close(d[1]); printf("%d\n", n); exit(0);}
 dup2(d[0], 0); close(d[0]); close(d[1]);
 s = 0; while(scanf("%d", &n) > 0) s += n;
 printf("%d\n", s);
 return 0;
}
