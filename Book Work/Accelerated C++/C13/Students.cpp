#include <algorithm>
#include <string>
#include <vector>
#include "grade.h"
#include "Students.h"

using std::istream;
using std::min;
using std::string;
using std::vector;

string Core::name() const { return n; }

double Core::grade() const {
  return ::grade(midterm, final, homework);
}

istream& Core::read_common(istream& in) {
  in >> n >> midterm >> final;
  return in;
}

istream& Core::read(istream& in) {
  read_common(in);
  read_hw(in, homework);
  return in;
}


double Grad::grade() const {
  return min(Core::grade(), thesis);
}

istream& Grad::read(istream& in) {
  read_common(in);
  in >> thesis;
  read_hw(in, homework);
  return in;
}

istream& read_hw(istream& in, vector<double>& hw) {
  if (in) {
    //get rid of previous contents
    hw.clear();

    double x;
    while (in >> x) {
      hw.push_back(x);
    }

    //clear the stream so that input will work for next student
    in.clear();
  }
  return in;
}

bool compare(const Core& c1, const Core& c2) {
  return c1.name() < c2.name();
}

bool compare_Core_ptrs(const Core* cp1, const Core* cp2) {
  return compare(*cp1, *cp2);
}
