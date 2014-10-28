#include <algorithm>
#include <cctype>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

bool not_url_char(char c) {
	static const string url_ch = "~;/?:@=&$-_.+!*'(),";
	
	return !(isalnum(c) || find(url_ch.begin(), url_ch.end(), c) != url_ch.end());
}

string::const_iterator url_beg(string::const_iterator b, string::const_iterator e) {
	static const string sep = "://";
	
	typedef string::const_iterator iter;
	iter i = b;
	
	while ((i = search(i, e, sep.begin(), sep.end())) != e) {
		//make sure seperator isn't at beginning or end of line
		if (i != b and i + sep.size() != e) {
			//beg marks beginning of protocol
			iter beg = i;
			while (beg != b and isalpha(beg[-1]))
				--beg;
		
			//is there at least one appropriate charater before and after seperator?
			if (beg != i and !not_url_char(i[sep.size()]))
				return beg;
		}
		i += sep.size();
	}
	return e;
}

string::const_iterator url_end(string::const_iterator b, string::const_iterator e) {
	return find_if(b, e, not_url_char);
}

vector<string> find_urls(const string& s) {
	vector<string> ret;
	typedef string::const_iterator iter;
	iter b = s.begin(), e = s.end();
	
	while (b != e) {
		//look for one or more letters followed by ://
		b = url_beg(b, e);
		
		//if found
		if (b != e) {
			//get rest of url
			iter after = url_end(b, e);
			ret.push_back(string(b, after));
			
			//advance and check for more urls
			b = after;
		}
	}
	return ret;
}

int main() {
	cout << "Enter a string: ";
	string s;
	getline(cin, s);
	
	vector<string> urls = find_urls(s);
	for(vector<string>::iterator it = urls.begin(); it != urls.end(); ++it) {
		cout << *it << endl;
	}
	return 0;
}