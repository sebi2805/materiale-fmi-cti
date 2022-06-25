#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
 
 
int main(int argc, char* argv[]) {




     int n = -1;
     pid_t pid;
   while(fork()){
        pid=getppid();
        printf("pid_curent: %d\n", pid);
       
        do{   
             if(n -=- 1) exit(n);
              } while(fork());
             }
             pid=getppid();
        printf("pid_curent: %d\n", pid);
   printf("%d\n", n);
    return 0;
}




//  r = mmap(NULL, sizeof *r, PROT_READ | PROT_WRITE, 
//                     MAP_SHARED | MAP_ANONYMOUS, -1, 0);


//     *r = 0;