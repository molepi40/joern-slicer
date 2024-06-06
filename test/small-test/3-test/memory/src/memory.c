#include <stdio.h>

struct s1 {
    int d;
};
struct s2 {
    struct s1 *p;
};

int main() {
    struct s1 data;
    struct s2 *sp;
    int a[2];
    sp = malloc(sizeof(struct s2));
    sp->p = &data;
    sp->p->d = 3;
    sp = a;
    a[1] = data.d;

    return 0;
}
