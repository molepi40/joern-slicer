struct A{
    int x;
    int y;
};

typedef struct A Point;

typedef struct B{
    Point p1;
    struct A p2;
}Line;

int main() {
    struct A p1;
    p1.x = 1;
    p1.y = 1;
    Point p2;
    p2.x = 2;
    p2.y = 2;

    struct B l1;
    Line l2;
    l1.p1 = p1;
    l1.p2 = p2;
    l2 = l1;
}