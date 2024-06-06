int x;
x = 2;

int main() {
    int y, z;
    y = x;
    
    if (x > 1) {
        x = 2;
    } else {
        x = 3;
    }

    y = y + x;
    z = x;
}