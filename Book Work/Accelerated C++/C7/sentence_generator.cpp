#include <algorithm>
#include <cctype>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using namespace std;

typedef vector<string> Rule;
typedef vector<Rule> Rule_collection;
typedef map<string, Rule_collection> Grammar;

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

Grammar read_grammar(istream& in) {
  Grammar ret;
  string line;
  
  while(getline(in, line)) {
    vector<string> entry = split(line);
    if(!entry.empty())
      ret[entry[0]].push_back(Rule(entry.begin()+1, entry.end()));
  }
  return ret;
}

bool bracketed(const string& s) {
  return s.size() > 1 and s[0] == '<' and s[s.size() - 1] == '>';
}

int nrand(int n) {
  if (n <= 0 || n > RAND_MAX)
    throw domain_error("Argument to nrand is out of range");
  
  const int bucket_size = RAND_MAX / n;
  int r;

  do r = rand() / bucket_size;
  while (r >= n);

  return r;
}

void gen_aux(const Grammar& g, const string& word, vector<string>& ret) {
  if(!bracketed(word)){
    ret.push_back(word);
  } 
  else {
    Grammar::const_iterator it = g.find(word);
    if (it == g.end())
      throw logic_error("empty rule");

    const Rule_collection& c = it->second;
    const Rule& r = c[nrand(c.size())];

    for(Rule::const_iterator i = r.begin(); i != r.end(); ++i)
      gen_aux(g, *i, ret);
  }
}

vector<string> gen_sentence(const Grammar& g) {
  vector<string> ret;
  gen_aux(g, "<sentence>", ret);
  return ret;
}

int main() {
  Grammar grammar = read_grammar(cin);

  for(int i = 0; i < 10; ++i) {
    vector<string> sentence = gen_sentence(grammar);

    vector<string>::const_iterator it = sentence.begin();
    if(!sentence.empty()) {
      cout << *it;
      ++it;
    }

    while (it != sentence.end()) {
      cout << " " << *it;
      ++it;
    }
    cout << endl;
  }
  return 0;
}
