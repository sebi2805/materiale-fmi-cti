//A16. (1 punct) Scrieti un program care afisaza valoarea variabilei de
//environment TERM, apoi o asigneaza la valoarea "vt52", apoi genereaza un
//        proges fiu (cu fork) care afisaza valoarea lui TERM mostenita.

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

int main() {

    char *term = getenv("TERM");

    if(!term) {
        printf("Nu exista env-ul in system\n");
        exit(0);
    } else {
        printf("%s\n", term);
        int envWrite = putenv("TERM=vt52");
        if(envWrite == -1) {
            printf("Nu s-a putut scrie env-ul in system\n");
            exit(0);
        }
    }

    if(!fork()) {
        term = getenv("TERM");
        printf("%s\n", term);
    }

    return 0;

}