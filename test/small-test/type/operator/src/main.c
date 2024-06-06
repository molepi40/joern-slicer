#include <stdio.h>

int main() {
  int sum1 = 100 + 50;        // 150 (100 + 50)
  int sum2 = sum1 + 250;      // 400 (150 + 250)
  int sum3 = sum2 + sum2;     // 800 (400 + 400)
  printf("%d\n", sum1);
  printf("%d\n", sum2);
  printf("%d\n", sum3);

  int x = 10;
  x += 5;
  printf("%d", x);

  int x = 5;
  int y = 3;
  printf("%d", x > y); // returns 1 (true) because 5 is greater than 3

  int x = 5;
  int y = 3;
  // Returns false (0) because ! (not) is used to reverse the result
  printf("%d", !(x > 3 && x < 10));

  return 0;
}