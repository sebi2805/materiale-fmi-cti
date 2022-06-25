#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include<string.h>
#include <errno.h>
 
       #include <pwd.h>

int main(int argc, char **argv){
   // argc 
          // char *eu;
           
 
   
  if(argc!=2) {
         errno=-1;
         perror("NU CONVINE");
  }
  else{
struct passwd *pw;
pw=getpwnam(*(argv+1));
//int i=0;
//  while( pw=getpwent()){
//   {printf("%s    ", pw->pw_gecos);
//  }

  
  
//  }
printf("%s", pw->pw_gecos )  ;      // pw.*
//   perror("Nu exista");

  }
}