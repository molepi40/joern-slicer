#include <stdio.h>

int main() {
  int x = 20;
  int y = 18;
  if (x > y)
    printf("x is greater than y");
  
  int time = 20;
  if (time < 18) {
    printf("Good day.");
  } else {
    printf("Good evening.");
  }

  if (time < 10) {
    printf("Good morning.");
  } else if (time < 20) {
    printf("Good day.");
  } else {
    printf("Good night.");
  }

  (time < 18) ? 
  printf("Good day.") : 
  printf("Good evening.");
}