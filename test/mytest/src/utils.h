#ifndef UTILS_H
#define UTILS_H

typedef struct {
    int r;
    int i;
} Complex;

Complex* add_complex(Complex* a, Complex* b);

#endif