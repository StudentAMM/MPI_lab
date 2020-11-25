from itertools import chain

import numpy as np

point = np.linspace(0.8, 1.8, 5, endpoint=True).tolist()
print(point)

# initializing string


k = 3
# initializing split index list
split_list = np.linspace(0, len(point), 5, endpoint=False).round()
split_list = split_list.astype(int).tolist()
print(split_list)

temp = zip(chain([0], split_list), chain(split_list, [None]))
res = list(point[i: j] for i, j in temp)[1:]

print("The splitted lists are : " + str(res))

A = float(input("input A: "))
B = float(input("input B: "))
eps = int(input("input eps: "))
n = int(input("input n: "))
point = np.linspace(A, B, n, endpoint=True).round().tolist()

# массив масивов с точками, которые отправляются другим процессам
split_list = np.linspace(0, len(point), k, endpoint=False).round()
split_list = split_list.astype(int).tolist()
print(split_list)
temp = zip(chain([0], split_list), chain(split_list, [None]))
array_to_share = list(point[i: j] for i, j in temp)[1:]
print(array_to_share)