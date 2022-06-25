#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <pwd.h>

int main( int argc, char* *argv )
  {
    struct passwd* pw;

    if( ( pw = getpwnam( argv[1] ) ) == NULL ) {
      fprintf( stderr, "getpwnam: unknown %s\n",
        argv[1] );
      return( EXIT_FAILURE );
    }
    printf( "login name  %s\n", pw->pw_name );
    printf( "user id     %d\n", pw->pw_uid );
    printf( "group id    %d\n", pw->pw_gid );
    printf( "home dir    %s\n", pw->pw_dir );
    printf( "login shell %s\n", pw->pw_shell );
    return( EXIT_SUCCESS );
  }