#include <stdio.h>

int main () {
    /*Declaramos una variable entera y guardamos en ella el valor 25*/
    int x = 25;

    /*Declaramos un puntero a entero. Inicialmente guardamos en p la dirección de x.*/
    int *p = &x;

    /*Imprimimos el valor directo de x.*/
    printf ("x = %d\n", x);

    //Imprimimos la direcciónn de x. El formato %p espera un puntero de tipo void.*/
    printf ("&x = %p\n", (void *)&x);

    //Imprimimos el contenido de p. Ese contenido es la dirección de x./
    printf ("p = %p\n", (void *)p);

    //Imprimimos el contenido de la dirección guardada en p/
    printf ("*p = %d\n", *p);
    
    return 0;
}
