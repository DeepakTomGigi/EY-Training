import numpy as np

# 1D array
arr1 = np.array([10, 20, 30, 40])

# 2D array
arr2 = np.array([[1,2,3],[4,5,6]])

print(arr1)
print(arr2)

marks = np.array([80, 75, 90, 85])

print(marks.max())
print(marks.min())
print(marks.mean())
# print(sum(marks))

data = np.array([10,20,30, 40])

print("First 3 elements:", data[:3])        #slicing
print("Reversed: ", data[::-1])             #reverse
print("Sum:",np.sum(data))
print("standard deviation:", np.std(data))
