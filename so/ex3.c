//
// D2. (4 puncte) Program care primeste ca argument in linia de comanda un
// director si calculeaza suma dimensiunilor fisierelor din arborescenta cu
// originea in el.
//

#include <stdio.h>
#include <sys/stat.h>
#include <dirent.h>
#include <string.h>

#define bytes_to_megabytes 1000000

long file_size(const char *input) {
    struct stat s;
    if(stat(input, &s) == -1) {
        return 0;
    } else {
        if(S_ISREG(s.st_mode))
            return s.st_size;
        else return 0;
    }
}

void calculate_sum(char *base, long *sum) {
    char new_path[500];
    struct dirent *dp;
    DIR *dir = opendir(base);
    if(!dir) {
        return;
    }
    while((dp = readdir(dir)) != NULL) {
        if(strcmp(dp -> d_name, ".") != 0 && strcmp(dp -> d_name, "..") != 0) {
            strcpy(new_path, base);
            strcat(new_path, "/");
            strcat(new_path, dp->d_name);
            *sum += file_size(new_path);
            calculate_sum(new_path, sum);
        }
    }
}

int main(int argc, char *argv[]){
    if(argc == 2) {
        long sum = 0;
        calculate_sum(argv[1], &sum);
        printf("%f MB\n", (float)sum/bytes_to_megabytes);
    } else if (argc < 2) {
        printf("Trebuie sa trimiti 1 numar ca argument!\n");
    } else {
        printf("Ai trimis mai mult de 1 numar ca argumente!\n");
    }
    return 0;
}
