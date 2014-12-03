#ifndef GUARD_students_h
#define GUARD_students_h

#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "Handle.h"

class Core {
 public:
  Core(): midterm(0), final(0) {}
  Core(std::istream& is) { read(is); }
  virtual ~Core() {}

  std::string name() const;

  virtual double grade() const;
  virtual std::istream& read(std::istream&);

 protected:
  std::istream& read_common(std::istream&);
  double midterm, final;
  std::vector<double> homework;
  
 public:
	virtual Core* clone() const { return new Core(*this); }
	
 private:
  friend class Student_info;
  std::string n;
};

class Grad: public Core {
 public:
  Grad(): thesis(0) {}
  Grad(std::istream& is) { read(is); }

  double grade() const;
  std::istream& read(std::istream&);
 private:
  double thesis;
  Grad* clone() const { return new Grad(*this); }
};

class Student_info {
 public:
  Student_info() {}
  Student_info(std::istream& is) { read(is); }
  
  std::istream& read(std::istream&);
  
  std::string name() const {
    if(cp)
      return cp->name();
    else throw std::runtime_error("uninitialized Student");
  }

  double grade() const {
    if (cp) return cp->grade();
    else throw std::runtime_error("uninitialized Student");
  }
 
  static bool compare(const Student_info& s1, const Student_info& s2) {
    return s1.name() < s2.name();
  }

 private:
  Handle<Core> cp;
};

std::istream& read_hw(std::istream&, std::vector<double>&);
bool compare(const Core&, const Core&);
bool compare_Core_ptrs(const Core*, const Core*);

#endif
