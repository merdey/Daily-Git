#include <iostream>
#include <memory>

using namespace std;

template <class T> class Vec {
public:
  typedef T* iterator;
  typedef const T* const_iterator;
  typedef size_t size_type;
  typedef T value_type;

  Vec() { create(); }
  explicit Vec(size_type n, const T& t = T()) { create(n, t); }
  
  Vec(const Vec& v) { create(v.begin(), v.end()); }
  Vec& operator=(const Vec&); //as defined in 11.3.2/196
  ~Vec() { uncreate(); }

  T& operator[](size_type i) { return data[i]; }
  const T& operator[](size_type i) const { return data[i]; }

  void push_back(const T& t) {
    if (avail == limit)
      grow();
    unchecked_append(t);
  }

  size_type size() const { return avail - data; }

  iterator begin() { return data; }
  const_iterator begin() const { return data; }

  iterator end() { return avail; }
  const_iterator end() const { return avail; }

private:
  iterator data;
  iterator avail;
  iterator limit;

  allocator<T> alloc;
  
  void create();
  void create(size_type, const T&);
  void create(const_iterator, const_iterator);

  void uncreate();

  void grow();
  void unchecked_append(const T&);
};

template <class T>
Vec<T>& Vec<T>::operator=(const Vec& rhs) {
  //check for self assignment
  if (&rhs != this) {
    uncreate();
    create(rhs.begin(), rhs.end());
  }
  return *this;
}

template <class T> 
void Vec<T>::create() {
  data = avail = limit = 0;
}

template <class T> 
void Vec<T>::create(size_type n, const T& val) {
  data = alloc.allocate(n);
  limit = avail = data + n;
  uninitialized_fill(data, limit, val);
}

template <class T> 
void Vec<T>::create(const_iterator i, const_iterator j) {
  data = alloc.allocate(j - i);
  limit = avail = uninitialized_copy(i, j, data);
}

template <class T> 
void Vec<T>::uncreate() {
  if (data) { // deallocate requires nonzero pointer (unlike delete)
    //destory (in reverse order) constructed elements
    iterator it = avail;
    while (it != data)
      alloc.destroy(--it);
    
    //return all space that was allocated
    alloc.deallocate(data, limit - data);
  }
  //reset pointers to indicate Vec is empty again
  data = limit = avail = 0;
}

template <class T>
void Vec<T>::grow() {
  size_type new_size = max(2 * (limit - data), ptrdiff_t(1));

  iterator new_data = alloc.allocate(new_size);
  iterator new_avail = uninitialized_copy(data, avail, new_data);
  //return old space
  uncreate();
  //reset pointers to point to newly allocated space
  data = new_data;
  avail = new_avail;
  limit = data + new_size;
}

template <class T>
void Vec<T>::unchecked_append(const T& val) {
  alloc.construct(avail++, val);
}

template <class T>
void print_vec(Vec<T>& v) {
  typedef typename Vec<T>::const_iterator const_it;
  for (const_it it = v.begin(); it != v.end(); ++it) {
    cout << *it << " ";
  }
  cout << endl;
}

int main() {
  Vec<char> test_vec(5, 'a');
  print_vec(test_vec);

  test_vec.push_back('b');
  test_vec.push_back('c');
  print_vec(test_vec);

  cout << test_vec[4] << test_vec[5] << test_vec[6] << endl; //"abc"
  
  return 0;
}

