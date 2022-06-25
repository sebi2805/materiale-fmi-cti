#define m_index 16
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
static int *r;
 
int main(int argc, char* argv[]) {


 r = mmap(NULL, sizeof *r, PROT_READ | PROT_WRITE, 
                    MAP_SHARED | MAP_ANONYMOUS, -1, 0);


    *r = 0;
    return 0;
}
// int cautare_fork(int a[], int *r, int search, int start, int end){
// if(start==end){
// if(*(a+end)==search){
//           return *r=*r+1;
// }
// // printf("%d ", *(a+start));

// return *r;

// }
// else 
// {pid_t child = fork();
// if (child == 0)
// {*r= cautare_fork(a, r, search, start, (start+end)/2);
 
//  }
//  else {pid_t child2 = fork();
//             if (child2 == 0)
//                *r= cautare_fork(a, r, search, (start + end)/2+1, end);
                
//   }


// }


// return *r;

// }
  //  char *p;
  //  long conv;
  //  int a[argc]  ;
  //  if(argc<=2) {
  //    errno=-1;
  //    perror("NU AM PRIMIT NUMERELE");
  //  }
  //  else  {
  //   for(int i=1; i<argc;i++){
  // conv = strtol(argv[i], &p, 10);  
  //    a[i]= conv;
     
  //      } 
  //      if(argc==3) {
  //        if( a[1]==a[2])printf("1");
  //        else printf("0");}
  //      else 
  //             printf("%d\n", cautare_fork(a,r, a[1], 2, argc));
  //  }