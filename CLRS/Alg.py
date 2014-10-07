##########
#DATA STRUCTURES
##########

class Stack:
    def __init__(self):
        self.last = None

    def push(self, value):
        newNode = Node(value)
        newNode.prev = self.last
        self.last = newNode

    def pop(self):
        value = self.last.value
        self.last = self.last.prev

        return value

class Node:
    def __init__(self, value):
        self.value = value
        self.prev = None


##########
#SORTING
##########

#http://stackoverflow.com/questions/18761766/mergesort-python
def mergeSort(x):
    #base case
    if len(x) < 2:
        return x
    result = []
    #compute mid, recursively call to generate left and right arrays
    mid = int(len(x) / 2)
    left = mergeSort(x[:mid])
    right = mergeSort(x[mid:])
    #combine left and right arrays
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            result.append(right[j])
            j += 1
        else:
            result.append(left[i])
            i += 1
    #add whichever side is left over and return
    #careful += != append()
    result += left[i:]
    result += right[j:]

    return result

def insertionSort(x):
    for j in range(1, len(x)):
        key = x[j]
        i = j - 1
        while (i >= 0 and x[i] < key):
            x[i + 1], x[i] = x[i], x[i + 1]
            i -= 1
        #x[i + 1] = key #not sure what this does but it was in the book


##########
#SEARCHING
##########
            
def linearSearch(x, val):
    #invariant: val is not in A[:i - 1] (to the left of i)
    for i in range(len(x)):
        if x[i] == val:
            return i
    return False

def binarySearch(x, val):
    low = 0
    high = len(x)
    while high >= low:
        mid = low + int((high - low) / 2)
        if val == x[mid]:
            return mid
        elif val > x[mid]:
            low = mid + 1
            if low == len(x):
                return False
        else: #val < x[mid]
            high = mid - 1
    return False

x = [1, -2, 5, 4, 2, 3, 8, 9, 20, 11, 15, 14, 16, 12, 0, -1]
x = mergeSort(x)
y = binarySearch(x, 5)

