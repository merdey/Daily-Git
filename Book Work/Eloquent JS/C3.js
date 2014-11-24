var min = function(x, y) {
  return x < y ? x : y;
}

var isEven = function(value) {
  if (value == 0)
    return true
  if (value == 1)
    return false;
  
  return value > 0 ? isEven(value - 2) : isEven(value + 2);
}

function countBs(s) {
  var Bs = 0;
  for (var i = 0; i < s.length; i++) {
    if (s.charAt(i) == "B")
      Bs++;
  }
  return Bs;
}   

function countChar(s, c) {
  var count = 0;
  for (var i = 0; i < s.length; i++) {
    if (s.charAt(i) == c)
      count++;
  }
  return count;
}

function findSolution(target) {
  function find(start, history) {
    if (start == target)
      return history;
    else if (start > target)
      return null;
    else
      return find(start + 5, "(" + history + " + 5)") ||
        	 find(start * 3, "(" + history + " * 3)");
  }
  return find(1, "1");
}