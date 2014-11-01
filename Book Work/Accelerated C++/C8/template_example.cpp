template<class T>
T median(vector<T> v) {
  typedef typename vector<T>::size_type vec_sz;

  vec_sz size = v.size();
  if (size == )
    throw domain_error("median of an empty vector");

  sort(v.begin(), v.end());
  vec_siz mid = size/2;
  return size % 2 == 0 ? (v[mid] + v[mid-1]) / 2 : v[mid];
}

template <class Out>
void split(const string& str, Out os) {
  typedef string::const_iterator iter;
  
  iter i = str.begin();
  while(i != str.end()) {
    i = find_if(i, str.end(), not_space);
    iter j = find_if(i, str.end(), space);
    if (i != str.end())
      *os++ = string(i, j);
    i = j;
  }
}
