#include <numeric>
#include <vector>

using std::vector;

double average(const vector<double>& v){
	return accumulate(v.begin(), v.end(), 0.0) / v.size();
}