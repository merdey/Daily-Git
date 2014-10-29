#include <algorithm>
#include <iomanip>
#include <ios>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include "grade.h"
#include "Student_info.h"
#include "median.h"

using namespace std;

bool did_all_hw(const Student_info& s) {
	return ((find(s.homework.begin(), s.homework.end(), 0)) == s.homework.end());
}

double grade_aux(const Student_info& s) {
	try{
		return grade(s);
	} catch (domain_error) {
		return grade(s.midterm, s.final, 0);
	}
}

double median_analysis(const vector<Student_info>& students) {
	vector<double> grades;
	
	transform(students.begin(), students.end(), back_inserter(grades), grade_aux);
	return median(grades);
}

void write_analysis(ostream& out, 
					const string& name,
					double analysis(const vector<Student_info>&),
					const vector<Student_info>& did,
					const vector<Student_info>& didnt) {
	out << name << ": median(did) = " << analysis(did) << ", median(didnt) = " << analysis(didnt) << endl;
}

int main() {
	vector<Student_info> did, didnt;
	Student_info student;
	while (read(cin, student)){
		if (did_all_hw(student))
			did.push_back(student);
		else
			didnt.push_back(student);
	}
	
	if (did.empty()) {
		cout << "No student did all the homework!" << endl;
		return 1;
	}
	if (didnt.empty()) {
		cout << "Every student did all the homework!" << endl;
		return 1;
	}
	
	write_analysis(cout, "median", median_analysis, did, didnt);
	//write_analysis(cout, "average", average_analysis, did, didnt);
	//write_analysis(cout, "median of homework turned in", optimistic_median_analysis, did, didnt);

	return 0;
}
