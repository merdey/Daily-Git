#include <algorithm>
#include <iostream>
#include <string>

using namespace std;

bool is_palindrome(const string& s){
	return equal(s.begin(), s.end(), s.rbegin());
}

int main() {
	cout << "Enter a string: ";
	string s;
	while(getline(cin, s)) {
		cout << is_palindrome(s) << endl;;
	}
	return 0;
}