#include <stdio.h>

int main()
{
    int x, y;
    int *p = &x;
    x = 3;
    *p = 4;
    y = x;

    return 0;
}
