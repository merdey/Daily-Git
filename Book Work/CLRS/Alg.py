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

class Queue:
    def __init__(self):
        self.first = None
        self.last = None

    def enqueue(self, value):
        newNode = Node(value)
        if not self.first:
            self.first = newNode
            self.last = newNode
        else:
            oldLast = self.last
            self.last = newNode
            oldLast.prev = self.last
    
    def dequeue(self):
        firstValue = self.first.value
        if self.first:
            self.first = self.first.prev
        else:
            self.first = None
        return firstValue

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
        else: #val < x[mid]
            high = mid - 1
    return False

#########
#CTCI
#########
def allUnique(string):
    for i in range(len(string) - 1):
        if string[i] in string[i + 1:]:
            return False
    return True

def reverseCString(string):
    reversedString = ''
    for i in range(len(string) - 2, -1, -1):
        reversedString += string[i]
    return reversedString + string[-1]

def anagram(string1, string2):
    count1 = countLetters(string1)
    count2 = countLetters(string2)
    return count1 == count2

def countLetters(string):
    count = {}
    for letter in string:
        if letter in count:
            count[letter] += 1
        else:
            count[letter] = 1
    return count
