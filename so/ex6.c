/*
 * A8. (1.5 puncte) Scrieti un program care genereaza un fiu cu fork iar acesta
 trimite tatalui un numar aleator de semnale SIGUSR1; fiul numara cate a
 trimis, tatal numara cate a primit, apoi fiecare afisaza numarul respectiv.
 Se va asigura protectia la pierderea unor semnale.
 */

#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
int nr=0;
sigset_t ms;

void h1_tata(int n){
    signal(n,h1_tata);
    kill(getppid(),SIGUSR1);
}

void h2_tata(int n){
    printf("Am primit: %d\n",nr);
    exit(0);}

void h1_fiu(int n){signal(n,h1_fiu);}

void h2_fiu(int n){printf("Am trimis: %d\n",nr); exit(0);}

int main(){
    sigemptyset(&ms); sigaddset(&ms,SIGUSR1);
    sigprocmask(SIG_SETMASK,&ms,NULL);
    sigfillset(&ms); sigdelset(&ms,SIGUSR1);
    if(fork() == 0) {
        signal(SIGUSR1,h1_fiu);
        signal(SIGINT,h2_fiu);
        for(int i=0;i<2000;++i){kill(getpid(),SIGUSR1); ++nr; sigsuspend(&ms);}
        printf("Am trimis: %d\n",nr);
    } else {
        signal(SIGUSR1,h1_tata);
        signal(SIGINT,h2_tata);
        sigdelset(&ms,SIGINT);
        while(1){sigsuspend(&ms); ++nr;}
    }

    return 0;
}