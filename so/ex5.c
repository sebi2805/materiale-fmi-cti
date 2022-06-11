/*
 * A1. (2 puncte) Scrieti un program "copy" care se va lansa sub forma:
     copy   f1 + ... + fn    f
 * (unde f1, ..., fn, f sunt fisiere) si are ca efect crearea lui f continand
 * concatenarea lui f1, ..., fn; daca n=1 se copiaza f1 in f. Se vor folosi
 * doar functiile de la nivelul inferior de prelucrare a fisierelor.
 */

#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>

void copiaza(int, char**);

int main(int argc, char *argv[])
{
    bool OK = 1;
    if(argc < 3) {
        printf("Prea putine argumente!\n");
        OK = 0;
    } else if (argc == 3) {
        for (int i = 1; i < 3; i++) {
            if (strcmp(argv[i], "+") == 0) {
                printf("Lipsa fisier sursa sau destinatie\n");
                OK = 0;
            }
        }
    } else if (argc > 3) {
            for(int i = 1 ; i < argc - 1 ; i+=2) {
                if(strcmp(argv[i], "+") == 0 || (strcmp(argv[i+1], "+") != 0 && i+1 != argc-1)) {
                    printf("Greseala apel program\n");
                    OK = 0;
                }
        }
    }

    if (OK) {
        copiaza(argc, argv);
    }

    return 0;
}

void copiaza(int argc, char *argv[]) {
    char* fisier_final = argv[argc-1];
    int fdfinal = open(fisier_final, O_WRONLY | O_APPEND);
    for(int i = 1 ; i < argc-1 ; i += 2) {
        int fd;
        if ((fd = open(argv[i], O_RDWR)) >= 0)
        {
            char c;
            while (read(fd, &c, 1) == 1) {
                write(fdfinal, &c, 1);
            }
        }
    }
    close(fdfinal);
}