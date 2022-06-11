//
// 6. (2 puncte) Cerinta (a).
//    (a) 2 programe, care se lanseaza de la terminale diferite de catre acelasi
//    utilizator, obtinand astfel 2 procese; fiecare proces va citi de la
//    tastatura PID-ul celuilalt.
//
//    Fiecare proces trimite celuilalt 2000 SIGUSR1, apoi
//    un SIGINT (care va determina terminarea procesului advers). Inainte de
//    terminare, fiecare proces scrie cate semnale a trimis si cate a primit.
//

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

int trimise = 0;
int primite = 0;
pid_t pa;
sigset_t ms;

void h1(int n){
    ++primite;
}

void h2(int n) {
    printf("\nAm primit %d, Am trimis %d\n", primite, trimise);
    exit(0);
}

int main() {
    signal(SIGUSR1, h1);
    signal(SIGINT, h2);
    sigemptyset(&ms);
    sigaddset(&ms,SIGUSR1);
    sigprocmask(SIG_SETMASK,&ms,NULL);
    printf("PROCESUL CURENT ARE NUMARUL - %d\n", getpid());
    printf("PROCESUL ADVERS: ");
    scanf("%d", &pa);
    sigfillset(&ms);
    sigdelset(&ms,SIGUSR1);
    sigdelset(&ms,SIGINT);
    for(int i = 0 ; i < 2000 ; i++) {
        kill(pa, SIGUSR1);
        ++trimise;
        sigsuspend(&ms);
    }
    printf("\nAm primit %d, Am trimis %d\n", primite, trimise);
}
