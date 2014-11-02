#include "grade.h"
#include "Student_info.h"

using std::istream;
using std::vector;

Student_info::Student_info(): midterm(0), final(0) {}
Student_info::Student_info(istream& is) { read(is); }

istream& Student_info::read(istream& in) {
in >> n >> midterm >> final;
read_hw(in, homework);
return in;
}

double Student_info::grade() const{
return ::grade(midterm, final, homework);
}

bool compare(const Student_info& x, const Student_info& y){
return x.name() > y.name();
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
