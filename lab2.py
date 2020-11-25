# mpiexec -n 4 python test.py
# Задание 2
# Требуется вычислить значения суммы ряда в и точках заданного ин-
# тервала [А,В] с точностью є. Процесс-мастер вводит с клавиатуры А, В, є и
# n, вычисляет аргументы х1=А, х2, … хn=В и рассылает каждому процессу
# n/k (k -- количество запущенных процессов) значений, используя функ-
# цию MPI Scatter и значение є с помощью функции MPI Bcast. Каждый
# процесс вычисляет значения функции в полученных точках и отправляет
# процессу-мастеру с помощью функции MPI Gather. Процесс - мастер вы-
# водит полученные результаты и точные значения функции в соответст-
# вующих точках в виде таблицы.

# 5) arcsin


from mpi4py import MPI
import numpy as np
from itertools import chain

comm = MPI.COMM_WORLD

rank = comm.Get_rank()
k = comm.Get_size()  # кол-во запущенных процесов
eps = 0
points_to_share = []

if rank == 0:
    # ввод данных
    A = float(input("input A: "))
    B = float(input("input B: "))
    eps = int(input("input eps: "))
    n = int(input("input n: "))
    # точки для которых надо рассчитать значение функции
    points = np.linspace(A, B, n, endpoint=True).tolist()

    # массив масивов с точками, которые отправляются другим процессам
    split_list = np.linspace(0, len(points), k, endpoint=False).round()
    split_list = split_list.astype(int).tolist()
    temp = zip(chain([0], split_list), chain(split_list, [None]))
    points_to_share = list(points[i: j] for i, j in temp)[1:]
    print(points_to_share)

# отправить данные всем процесам
eps = comm.bcast(eps, root=0)
points_to_share = comm.scatter(points_to_share, root=0)

# вычислить значения функции в точках
data = []
for point in points_to_share:
    data.append((point, np.math.asin(point)))

# отправить мастеру
data = comm.gather(data, root=0)

if rank == 0:
    # получение и вывод данных от других процессов
    for i in range(0, k):
        for (point, value) in data[i]:
            print(point, '', value)
