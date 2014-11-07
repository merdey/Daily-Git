#include <algorithm>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "Handle.h"
#include "Students.h"

using namespace std;

int main() {
  vector< Handle<Core> > students;
  Handle<Core> record;
  char ch;
  string::size_type maxlen = 0;

  while (cin >> ch) {
    if (ch == 'U')
      record = new Core;
    else
      record = new Grad;
    record->read(cin); //Handle<T>::-> then virtual call to read()
    maxlen = max(maxlen, record->name().size());
    students.push_back(record);
  }
  
  sort(students.begin(), students.end(), Handle<Core>::compare_Core_handles);

  for (vector< Handle<Core> >::size_type i = 0; i != students.size(); ++i) {
    //students[i] is a Handle which we dereferencee to call the functions
    cout << students[i]->name()
	 << string(maxlen + 1 - students[i]->name().size(), ' ');
    try {
      double final_grade = students[i]->grade();
      streamsize prec = cout.precision();
      cout << setprecision(3) << final_grade
	   << setprecision(prec) << endl;
    } catch (domain_error e) {
      cout << e.what() << endl;
    }
  }

  return 0;
}
