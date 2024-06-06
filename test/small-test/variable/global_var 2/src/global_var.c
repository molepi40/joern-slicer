#include <stdio.h>
//This is a global variable
int num1;
num1 = 99;

int num2 = 100;

int num3;

void myfunction()
{
  printf("%d\n" , num1);
}
void myfunction2()
{
  printf("%d\n" , num2);
}
void myfunction3()
{
  num3 = 101;
  printf("%d\n", num3);
}
int main() {
  myfunction();
  myfunction2();
  myfunction3();
  return 0;
}