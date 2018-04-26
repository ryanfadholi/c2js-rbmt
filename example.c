#include<stdio.h>

int main() {
    printf("Hello World!");


    /*
    __++ ** --&$
    This a multiline comment asdasdsadasdasdasdasdasdsa
    sadsadasdasdsad
    sadasdasdsadsa
    int i = 1;
    */

    if (2 
    //Wow, it's a first comment!
    //This is the second comment.
    == 2)
     {
    //This is a comment; and this is another;
    //
    /**/
    int i /*@@@@@how about
    //srts
    this? */
     = 2  ;
     }
    for(i         =1;i<5;i++){
        printf     (     "This is an arbitrarily long string *designed to test* the string joiner %d. %s ",  i, "Whoaaa. is this another string???");
        printf("Hmmmm \" I escaped some string here %c",'\'');
    }
    return 0;
}