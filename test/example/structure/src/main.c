#include <stdio.h>

// Create a structure called myStructure
struct myStructure {
  int myNum;
  char myLetter;
  char myString[30]; // String
};

int main() {
  // Create a structure variable of myStructure called s1
  struct myStructure s1;

  // Assign values to members of s1
  s1.myNum = 13;
  s1.myLetter = 'A';
  strcpy(s1.myString, "Some text");

  struct myStructure s2 = {14, 'B', "Some text"};

  struct myStructure s3 = s2;
  s3.myNum = 15;
  s3.myLetter = 'C';
  
  // Print values
  printf("s1 number: %d\n", s1.myNum);
  printf("s2 letter: %c\n", s2.myLetter);
  printf("s3 string: %s\n", s3.myString);

  return 0;
}