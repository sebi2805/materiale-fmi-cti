/*
F3. (2.5 puncte) Scrieti un program care primeste ca argument in linia de
 comanda un intreg si afisaza descompunerea sa in factori primi.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void factori_primi(int x){
    int d = 2;
    if(x < 0) {
        printf("Nu are sens numar negativ!\n");
        return;
    }
    printf("%d = ", x);
    if(x <= 1) {
        printf("%d\n", x);
        return;
    }
    while (x > 1) {
        int exp = 0;
        while(x % d == 0) {
            exp++;
            x /= d;
        }
        if(exp) {
            if(exp == 1) {
                if(x == 1) {
                    printf("%d\n", d);
                } else {
                    printf("%d * ", d);
                }
            } else {
                if(x == 1) {
                    printf("%d^%d\n", d, exp);
                } else {
                    printf("%d^%d * ", d, exp);
                }
            }
        }
        d++;
    }
}

bool valid_number(char *input){
    for(int i = 0 ; i < strlen(input) ; i++) {
        if(input[i] < '0' || input[i] > '9') {
            return false;
        }
    }
    return true;
}

int main(int argc, char *argv[]){
    if(argc == 2) {
        if(!valid_number(argv[1])) {
            printf("Argumentul 1 nu este un numar!\n");
        } else {
            factori_primi(atoi(argv[1]));
        }
    } else if (argc < 2) {
        printf("Trebuie sa trimiti 1 numar ca argument!\n");
    } else {
        printf("Ai trimis mai mult de 1 numar ca argumente!\n");
    }
    return 0;
}