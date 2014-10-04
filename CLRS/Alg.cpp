#include <iostream>

using namespace std;

void insertionSort(int arr[], int size) {
  for (int j = 1; j < size; ++j) {
    int key = arr[j];
    int i = j - 1;
    while (i >= 0 and arr[i] > key) {
      int temp = arr[i + 1];
      arr[i + 1] = arr[i];
      arr[i] = temp;
      
      i -= 1;
    }
  }
}

void printArray(int arr[], int size) {
  for (int i = 0; i < size; ++i) {
    cout << arr[i] << endl;
  }
  cout << endl;
}

int main(){
  int test[] = {1, 4, 5, 0, 2, 3};
  printArray(test, 6);
  return 0;
}
