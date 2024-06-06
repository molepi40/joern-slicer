#include <stdio.h>
#include "utils.h"

int main() {
    int x;
    printf("%c", x);

    Complex a, b;
    Complex* c;
    c = add_complex(&a, &b);
    printf("%d + %di", c->r, c->i);
}