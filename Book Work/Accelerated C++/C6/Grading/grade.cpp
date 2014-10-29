#include <algorithm>
#include <stdexcept>
#include <vector>
#include "average.h"
#include "grade.h"
#include "median.h"
#include "Student_info.h"

using std::domain_error;
using std::vector;

double grade(double midterm, double final, double homework) {
  return 0.2 * midterm + 0.4 * final + 0.4 * homework;
}

double grade(double midterm, double final, const vector<double>& hw) {
  if (hw.size() == 0) {
    throw domain_error("studen has done no homework");
  }
  return grade(midterm, final, median(hw));
}

double grade(const Student_info& s) {
  return grade(s.midterm, s.final, s.homework);
}

double average_grade(const Student_info& s){
	return grade(s.midterm, s.final, average(s.homework));
}

double grade_aux(const Student_info& s) {
	try{
		return grade(s);
	} catch (domain_error) {
		return grade(s.midterm, s.final, 0);
	}
}

double optimistic_median(const Student_info& s) {
	vector<double> nonzero;
	remove_copy(s.homework.begin(), s.homework.end(), 
			back_inserter(nonzero), 0);
			
	if (nonzero.empty())
		return grade(s.midterm, s.final, 0);
	else
		return grade(s.midterm, s.final, median(nonzero));
}