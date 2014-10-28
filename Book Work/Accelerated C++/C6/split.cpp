#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

bool space(char c) {
	return isspace(c);
}

bool not_space(char c) {
	return !isspace(c);
}

vector<string> split(const string& str) {
	typedef string::const_iterator iter;
	vector<string> ret;
	
	iter i = str.begin();
	while (i != str.end()) {
		//ignore leading blanks
		i = find_if(i, str.end(), not_space);
		
		//find end of next word
		iter j = find_if(i, str.end(), space);
		
		//copy characters in [i,j)
		if(i != str.end())
			ret.push_back(string(i, j));
		i = j;
	}
	return ret;
}

int main() {
	cout << "Enter a string: ";
	string s;
	getline(cin, s);
	
	vector<string> words = split(s);
	for(vector<string>::iterator it = words.begin(); it != words.end(); ++it) {
		cout << *it << endl;
	}
	return 0;
}