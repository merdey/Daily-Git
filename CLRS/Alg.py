def insertionSort(A):
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1
        while (i >= 0 and A[i] < key):
            A[i + 1], A[i] = A[i], A[i + 1]
            i -= 1
        #A[i + 1] = key #not sure what this does

def linearSearch(A, val):
    #invariant: val is not in A[:i - 1] (to the left of i)
    for i in range(len(A)):
        if A[i] == val:
            return i
    return False
        
A = [1, -2, 5, 4, 2, 3, 8, 9, 20, 11, 15, 14, 16, 12, 0, -1]
print(A)
print(linearSearch(A, 5))
