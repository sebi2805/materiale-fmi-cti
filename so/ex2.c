//
// F8. (0.5 puncte) Simularea comenzii "cp" in forma cea mai simpla: program
// ce copiaza un fisier intr-alt fisier; specificatorii fisierelor sunti dati
// ca argumente in linia de comanda.
//

#include <stdio.h>
#include <stdlib.h>

void cp(char* input, char* output) {
    FILE* in = fopen(input, "r");
    if(in == NULL) {
        printf("Fisierul input nu este gasit!\n");
        exit(EXIT_FAILURE);
    }
    FILE* out = fopen(output, "w");
    if(out == NULL) {
        printf("Nu s-a putut crea fisierul output!\n");
        exit(EXIT_FAILURE);
    }
    char ch;
    while((ch = fgetc(in)) != EOF) {
        fputc(ch, out);
    }
    printf("Fisier copiat!");
    fclose(in);
    fclose(out);
}

int main(int argc, char *argv[]) {
    if(argc == 3) {
        cp(argv[1], argv[2]);
    } else if (argc < 3) {
        printf("Trebuie sa trimiti 2 path-uri ca argumente!\n");
    } else {
        printf("Ai trimis mai mult de 2 path-uri ca argumente!\n");
    }
    return 0;
}