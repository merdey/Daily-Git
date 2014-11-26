//Exercise 1
function range(start, end, step) {
  a = [];
  if (!step)
    var step = 1;
  if (step > 0){
  	for (var i = start; i <= end; i += step)
    	a.push(i);
  }
  else {
    for (var i = start; i >= end; i += step)
    	a.push(i);
  }
  return a;
}

function sum(a) {
  s = 0;
  for (var e in a){
    s += a[e];
  }
  return s;
}

//Exercise 2
function reverseArray(a) {
  new_array = [];
  for (var i = a.length - 1; i >= 0; i--)
    new_array.push(a[i]);
  return new_array;
}

function reverseArrayInPlace(a) {
  for (var i = 0; i < a.length / 2; i++) {
    temp = a[i];
    a[i] = a[(a.length - 1) - i]
    a[(a.length - 1) - i] = temp;
  }
}

//Exercise 3
function arrayToList(a) {
  if (a.length == 1) 
    return {
		value :  a[0],
		rest : null
	};
    
  return {
    	value: a[0],
    	rest : arrayToList(a.slice(1))
  };
}

function listToArray(list) {
  var a = [];
  while (list.rest) {
    a.push(list.value);
    list = list.rest;
  }
  a.push(list.value);
  return a;
}

function prepend(v, list) {
  return {
    value: v,
    rest: list
  };
}

function nth(list, n) {
  if (n == 0) 
    return list.value;
  
  return nth(list.rest, n - 1);
}