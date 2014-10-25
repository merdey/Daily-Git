/* list example, not used
list<Student_info> extract_fails(list<Student_info>& students){
	list<Student_info> fail;
	list<Student_info>::iterator iter = students.begin();
	while (iter != students.end()) {
		if (fgrade(*iter)) {
			fail.push_back(*iter);
			iter = students.erase(iter);
		}
		else {
			++iter;
		}
	}
	return fail;
}

bool fgrade(const Student_info& s){
	return grade(s) < 60;
}
*/

#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

vector<string> split(const string& s) {
	vector<string> ret;
	typedef string::size_type string_size;
	string_size i = 0;
	
	while (i != s.size()) {
		//set i to index at beginning of word
		while ( i != s.size() and isspace(s[i])) {
			++i;
		}
		//set j to end of word
		string_size j = i;
		while (j != s.size() and !isspace(s[j])) {
			j++;
		}
		if (i != j) {
			ret.push_back(s.substr(i, j-1));
			i = j;
		}
	}
	return ret;
}

int main(){
	string s;
	while (getline(cin, s)) {
		vector<string> v = split(s);
		
		for (vector<string>::size_type i = 0; i != v.size(); ++i) {
			cout << v[i] << endl;
		}
	}
	return 0;
}
		