#include <stdlib.h>
#include "utils.h"

Complex* add_complex(Complex* a, Complex* b) {
    Complex* c = (Complex*)malloc(sizeof(Complex));
    c->r = a->r + b->r;
    c->i = a->i + b->i;
}