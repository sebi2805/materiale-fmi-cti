#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/limits.h>
#include<string.h>
extern char **environ; 
 
int main(int argc, char *argv[], char *envp[])
{
          char s[30]="";
// int i=0;
//     while(*(envp+i)){
              
// strcat(*(envp+i+1), *(envp+i));
//       strcpy(*(s+i), *(envp+i+1));


// strcpy(s, " =5\0");
      clearenv();
     int x=5;
//       putenv(s);
//       i=0;
//       while(*s){
//        putenv(*(s+i));
//        i++;}

 while(*envp)     // *(x+1)   *(*(x+1))
        printf("%s\n",*envp++);

}

//   char *s="";
//   char **p=environ;
//  int i;

for (i=0; *(p+i);i+=2 ) {
    printf("%s%S\n", *(p+i+1), *(p+i));
     
//   }
//   printf("\n\n\n");
//   for (i=0; *(p+i);i++ ) {
   
//    if(i%2==1) {strcpy(s, "");
//     setenv(**(p+i), s, 1);}
//    if(i%2==0) {strcat(*(p+i+1), *(p+i));
//              strcpy(s,*(p+i+1)  );
//     setenv(**(p+i+1), s, 1);}
//     //printf("%s%s\n", *(p+i+1), *(p+i));
     
//   }