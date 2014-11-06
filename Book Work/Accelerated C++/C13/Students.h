#ifndef GUARD_students_h
#define GUARD_students_h

#include <iostream>
#include <string>
#include <vector>

class Core {
 public:
  Core(): midterm(0), final(0) {}
  Core(std::istream& is) { read(is); }

  std::string name() const;

  virtual double grade() const;
  virtual std::istream& read(std::istream&);
 protected:
  std::istream& read_common(std::istream&);
  double midterm, final;
  std::vector<double> homework;
 private:
  std::string n;
};

class Grad : public Core {
 public:
  Grad(): thesis(0) {}
  Grad(std::istream& is) { read(is); }

  double grade() const;
  std::istream& read(std::istream&);
 private:
  double thesis;
};

std::istream& read_hw(std::istream&, std::vector<double>&);
bool compare(const Core&, const Core&);
bool compare_Core_ptrs(const Core*, const Core*);

#endif
