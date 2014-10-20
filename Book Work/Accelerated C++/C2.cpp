#include <iostream>
#include <string>

using namespace std;

int main(){
  cout << "Please enter you first name: ";
  string name;
  cin >> name;
  
  const string greeting = "Hello, " + name + "!";

  cout << "Enter vertical padding: ";
  int vertical_pad;
  cin >> vertical_pad;
  cout << "Enter horizontal padding: ";
  int horizontal_pad = 10;
  cin >> horizontal_pad;
  const int rows = vertical_pad * 2 + 3;
  const string::size_type cols = greeting.size() + horizontal_pad * 2 + 2;
  
  cout << endl;
  for (int r = 0; r != rows; ++r) {
    string::size_type c = 0;
    while (c != cols) {
      //is it time to write the greeting?
      if (r == vertical_pad + 1 && c == horizontal_pad + 1) {
	cout << greeting;
	c += greeting.size();
      }
      else {
	//are we on the border?
	if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) {
	  cout << "*";
	}
	else {
	  cout << " ";
	}
	++c;
      }
    }
    cout << endl;
  }

  return 0;
}
