#include <algorithm>
#include <cctype>
#include <iterator>
#include <iostream>
#include <string>

using namespace std;

bool space(char c) {
	return isspace(c);
}

bool not_space(char c) {
	return !isspace(c);
}

template <class Out>
void split(const string& str, Out os) {
  typedef string::const_iterator iter;
  
  iter i = str.begin();
  while(i != str.end()) {
    i = find_if(i, str.end(), not_space);
    iter j = find_if(i, str.end(), space);
    if (i != str.end())
      *os++ = string(i, j);
    i = j;
  }
}

int main() {
	string s;
	while(getline(cin, s)) {
		split(s, ostream_iterator<string>(cout, "\n"));
	}
	
	return 0;
}
