#include "Picture.h"

using namespace std;

Pic_base::wd_sz String_Pic::width() const {
  Pic_base::wd_sz n = 0;
  for (Pic_base::ht_sz i = 0; i != data.size(); ++i) {
    n = max(n, data[i].size());
  }
  return n;
}

Picture frame(const Picture& pic) {
  return new Frame_Pic(pic.p);
}

Picture hcat(const Picture& l, const Picture& r) {
  return new HCat_Pic(l.p, r.p);
}

Picture vcat(const Picture& t, const Picture& b) {
  return new VCat_Pic(t.p, b.p);
}

Picture::Picture(const vector<string>& v): p(new String_Pic(v)) {}

ostream& operator<<(ostream& os, const Picture& picture) {
  const Pic_base::ht_sz ht = picture.p->height();
  for (Pic_base::ht_sz i = 0; i != ht; ++i) {
    picture.p->display(os, i, false);
    os << endl;
  }
  return os;
}

