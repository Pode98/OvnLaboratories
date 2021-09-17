import numpy as np

num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))
product = num1 * num2

if product <= 1000:
    result = product
else:
    result = num1 + num2
print("The result is", result)

num = 10
print("Printing current and previous number sum in a given range")
prev = 0
for curr in range(num):  # type: int
    tot = curr + prev
    print('Sum:', tot)
    prev = curr

num_list = [10, 20, 30, 40, 10]  # Arbitrary list
first_element = num_list[0]
last_element = num_list[-1]
print("Are the firt element and last elements of the list {num_list} the same?")
if first_element == last_element:
    result = True
else:
    result = False
print(result)

num_list = [10, 20, 33, 46, 55]
print("Finding numbers divisible by 5 in the list {num_list}...")
for num in num_list:
    if num % 5 == 0:
        print(num)

statement = 'Emma is good developer. Emma is also a writer.'
count = 0
for i in range(len(statement) - 1):
    count += statement[i:i + 4] == 'Emma'
    print('Emma appeared', count, 'times')

list1 = [10, 20, 23, 11, 17]
list2 = [13, 43, 24, 36, 12]
list3 = []
for num in list1:
    if num % 2 != 0:
        list3.append(num)
for num in list2:
    if num % 2 == 0:
        list3.append(num)
print('The merged list is', list3)


s1 = 'OpenNets'
s2 = 'Optical'
middle_index = int(len(s1) / 2)
print('Original strings are', s1, s2)
middle_three = s1[:middle_index] + s2 + s1[middle_index:]
print('\nAfter appending the new string in the middle', middle_three)

s1 = 'America'
s2 = 'Japan'
s3 = s1[:1] + s2[:1] + s1[int(len(s1) / 2):int(len(s1) / 2) + 1] +s2[int(len(s2) / 2):int(len(s2) / 2) + 1] + s1[len(s1) - 1] +s2[len(s2) - 1]
print('Mix string is', s3)

print('Total counts of chars , digits , and symbols.')
input_string='P@#yn26at^&i5ve'
char_count = 0
digit_count = 0
symbol_count = 0
for char in input_string:
    if char.islower() or char.isupper():
        char_count += 1
    elif char.isnumeric():
        digit_count += 1
    else:
        symbol_count += 1
print('Chars = {char_count}\tDigits = {digit_count}\t Symbols = {symbol_count}')


input_string = "Welcome to USA. Awesome usa, isn\'t it?"
substring = 'USA'
temp_string = input_string.lower()
count = temp_string.count(substring.lower())
print('The {substring} count is:', count)


input_str = 'English = 78 Science = 83 Math = 68 History = 65'
words = input_str.split()
mark_list = [int(num) for num in words if num.isnumeric()]
total_marks = sum(mark_list)
percentage = total_marks / len(mark_list)
print('Mark total is {total_marks}\tAverage is {percentage}')


input_str = 'pynativepynvepynative'
count_dict = dict()
for char in input_str:
    count = input_str.count(char)
count_dict[char] = count
print(count_dict)


list1 = [3, 6, 9, 12, 15, 18, 21]
list2 = [4, 8, 12, 16, 20, 24, 28]
list3 = list()
odd_elements = list1 [1::2]
print('Element at odd-index positions from list 1')
print(odd_elements)
even_element = list2 [0::2]
print('Element at even-index positions from list 2')
print(even_element)
print('Printing final list 3')
list3.extend(odd_elements)
list3.extend(even_element)
print(list3)


sample_list = [34, 54, 67, 89, 11, 43, 94]
print('Original list', sample_list)
element = sample_list.pop(4)
print('List after removing element at index 4', sample_list)
sample_list.insert(2-1, element)
print('List after adding element at index 2', sample_list)
sample_list.append(element)
print('List after adding element at last', sample_list)

sample_list = [11, 45, 8, 23, 14, 12, 78, 45, 89]
print('Original list', sample_list)
length = len(sample_list)
chunk_size = int(length / 3)
start = 0
end = chunk_size
for i in range(1, chunk_size+1):
    indexes = slice(start, end, 1)
    list_chunk = sample_list[indexes]
    print('Chunk ', i, list_chunk)
    print('After reversing it ', list(reversed(list_chunk)))
    start = end
    if i < chunk_size:
        end += chunk_size
    else:
        end += length - chunk_size


sample_list = [11, 45, 8, 11, 23, 45, 23, 45, 89]
print('Original list', sample_list)
count_dict = dict()
for item in sample_list:
    if item in count_dict:
        count_dict[item] += 1
    else:
        count_dict[item] = 1
print('Printing count of each item', count_dict)


list1 = [2, 3, 4, 5, 6, 7, 8]
list2 = [4, 9, 16, 25, 36, 49, 64]
print('First list', list1)
print('Second list', list2)
result = zip(list1 , list2)
result_set = set(result)
print(result_set)


set1 = {23, 42, 65, 57, 78, 83, 29}
print('First set', set1)
set2 = {57, 83, 29, 67, 73, 43, 48}
print('Second set', set2)
intersection = set1.intersection(set2)
print('Intersection is', intersection)
for item in intersection:
    set1.remove(item)

set1 = {57, 83, 29}
print('First set', set1)
set2 = {57, 83, 29, 67, 73, 43, 48}
print('Second set', set2)
print('First set is subset of second set -', set1.issubset(set2))
print('Second set is subset of First set -', set2.issubset(set1))
print('First set is Super set of second set -', set1.issuperset(set2))
print('Second set is Super set of First set -', set2.issuperset(set1))
if set1.issubset(set2):
    set1.clear()
if set2.issubset(set1):
    set2.clear()
print('First set', set1)
print('Second set', set2)


roll_number = [47, 64, 69, 37, 76, 83, 95, 97]
sample_dict = {'Jhon': 47, 'Emma': 69, 'Kelly': 76, 'Jason': 97}
print('List -', roll_number)
print('Dictionary -', sample_dict)
roll_number[:] = [item for item in roll_number if item in sample_dict.values()]
print('After removing unwanted elements from list', roll_number)

speed = {'jan': 47, 'feb': 52, 'march': 47, 'April': 44, 'May': 52, 'June': 53, 'july': 54, 'Aug': 44, 'Sept': 54}
print('Dictionary\'s values -', speed.values())
speed_list = list()
for item in speed.values():
    if item not in speed_list:
        speed_list.append(item)
print('Unique list', speed_list)



sample_list = [87, 52, 44, 53, 54, 87, 52, 53]
print('Original list', sample_list)
sample_list = list(set(sample_list))
print('Unique list', sample_list)
tup = tuple(sample_list)
print('Tuple', tup)
print('Minimum number is:', min(tup))
print('Maximum number is:', max(tup))


array1 = np.empty([4, 2], dtype=np.uint16)
print('Printing array')
print(array1)
print('\nPrinting numpy array attributes')
print('1. Array Shape is', array1.shape)
print('2. Array dimensions are', array1.ndim)
print('3. Length of each element of array in bytes is', array1.itemsize)


print('Creating 5X2 array using np.arange method')
sample_array = np.arange(100, 200, 10) # start, stop, step # #
sample_array = sample_array.reshape(5, 2)
print(sample_array)

sample_array = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
print('Printing Input Array')
print(sample_array)
print('\nPrinting array of items in the third column from all rows')
new_array = sample_array[:, 2]
print(new_array)



sample_array = np.array([[3, 6, 9, 12], [15, 18, 21, 24], [27, 30, 33, 36], [39, 42, 45, 48], [51, 54, 57, 60]])
print('Printing Input Array')
print(sample_array)
print('\nPrinting array of odd rows and even columns')
new_array = sample_array[::2, 1::2]
print(new_array)


array1 = np.array([[5, 6, 9], [21, 18, 27]])
array2 = np.array([[15, 33, 24], [4, 7, 1]])
result_array = array1 + array2
print('The sum of the two arrays is')
print(result_array)
for num in np.nditer(result_array , op_flags=['readwrite']):
    num[...] = np.sqrt(num)
print('\nThe result array after calculating the square root of all elements')
print(result_array)

sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
print('Original array')
print(sample_array)
print('\nOne-line array')
line_array = sample_array.reshape(1, np.prod(sample_array.shape))
print(line_array)
print('\nOne-line sorted array')
sort_line_array = np.sort(line_array)
print(sort_line_array)
print('\nResult array')
sort_array = sort_line_array.reshape(sample_array.shape)
print(sort_array)

sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
print('Printing Original array')
print(sample_array)
min_of_axis1 = np.amin(sample_array , 1)
print('\nPrinting amin Of Axis 1')
print(min_of_axis1)
max_of_axis1 = np.amax(sample_array , 0)
print('Printing amax Of Axis 0')
print(max_of_axis1)

new_column = [10,10,10]
sample_array = np.array([[34, 43, 73], [82, 22, 12], [53, 94, 66]])
print('Printing Original array')
print(sample_array)
print('Array after deleting column 2 on axis 1')
sample_array = np.delete(sample_array , 1, axis=1)
print(sample_array)
arr = np.array([[10, 10, 10]])
print('Array after inserting column 2 on axis 1')
sample_array = np.insert(sample_array, 1, arr, axis=1)
print(sample_array)
