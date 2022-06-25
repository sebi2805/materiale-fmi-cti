#include <conio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
 #include <pwd.h>
  
 
int main(int argc, char **argv) {

          int check;
    char* dirname = getpwnam();
    clrscr();
    errno = 0;
    check = mkdir(dirname,0777);
  
     
    if (!check)
        printf("Succes a fost creat\n");
    else {
        printf("nu poate fi creat\n");
        exit(1);
    }
    switch (errno) {
            case EACCES :
                printf("nu permite scrierea");
                exit(EXIT_FAILURE);
            case EEXIST:
                printf("deja exista");
                exit(EXIT_FAILURE);
            case ENAMETOOLONG:
                printf("prea lung path");
                exit(EXIT_FAILURE);
            default:
                perror("mkdir");
                exit(EXIT_FAILURE);
        }
  
    getch();
  
    system("dir");
    getch();
}
 