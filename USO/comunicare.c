#include <sys/types.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <setjmp.h>
sigjmp_buf jb;
void h(int n) {signal(n, h); siglongjmp(jb, 1);}
int main(){
char tubp[11], tuba[11], buf[PATH_MAX], *mes, chr;
uint8_t pachet[PIPE_BUF];
int dp, da[10], na, len, i;
pid_t pid;
printf("Dati tubul propriu (max.10 car.): ");
fgets(buf, PATH_MAX, stdin); sscanf(buf, "%10s", tubp); fflush(stdin);
if(mkfifo(tubp, S_IRUSR | S_IWUSR | S_IWGRP | S_IWOTH) == -1)
{perror(tubp); return -1;}
strcpy((char *)pachet, tubp); strcat((char *)pachet, ": ");
len = (PIPE_BUF - strlen((char *) pachet) * sizeof(char)) / sizeof(char);
mes = (char *) (pachet + strlen((char *) pachet) * sizeof(char));
if(fork()) dp = open(tubp, O_RDONLY); else {dp = open(tubp, O_WRONLY); return 1;}
open(tubp, O_WRONLY);
printf("Tubului propriu este: %s\n", realpath(tubp, buf));
printf("Dati tuburile adverse (max.10), unul pe linie, o linie goala la sfarsit:\n");
for(na = 0; na < 10; ++na) {
fgets(buf, PATH_MAX, stdin); if(strcmp(buf, "\n") == 0) break;
sscanf(buf, "%10s", tuba); fflush(stdin);
if((da[na] = open(tuba, O_WRONLY)) == -1) {perror(tuba); --na;}
}
printf("Incepe conversatia:\n");
if(pid = fork()){
signal(SIGPIPE, h);
while(na && fgets(mes, len, stdin) != NULL) {
fflush(stdin);
if(mes[strlen(mes) - 1] != '\n') mes[strlen(mes) - 1] = '\n';
for(i = 0; i < na; ++i)
if(sigsetjmp(jb, 1)) {close(da[i]); --na; if (i < na) {da[i] = da[na]; --i;}}
else write(da[i], pachet, strlen((char *) pachet) * sizeof(char));
}
kill(pid, SIGKILL); while(wait(NULL) != -1); unlink(tubp);
} else {
while(1) {read(dp, &chr, sizeof(char)); write(1, &chr, sizeof(char));}
}
return 0;
}