# mpiexec -n 4 python lab2.py
# Задание 2
# Требуется вычислить значения суммы ряда в точках заданного
# интервала [А,В] с точностью eps. Процесс-мастер вводит с клавиатуры
# А, В, є и # n, вычисляет аргументы х1=А, х2, … хn=В и рассылает
# каждому процессу # n/k (k -- количество запущенных процессов) значений,
# используя функцию MPI Scatter и значение є с помощью функции MPI_Bcast.
# Каждый процесс вычисляет значения функции в полученных точках и отправляет
# процессу-мастеру с помощью функции MPI_Gather. Процесс-мастер
# выводит полученные результаты и точные значения функции в соответствующих
# точках в виде таблицы.

# 5) arcsin

# eps - до скольки знаков считать правильно после запятой

from mpi4py import MPI
import numpy as np
from itertools import chain
from decimal import Decimal
from decimal import getcontext


def my_arcsin(x, eps):
    n = Decimal(0)
    a = x
    arcsin = x
    E = 0.1 / (10 ** eps)
    while abs(a) > E:
        a *= (x * x * (2 * n + 1) * (2 * n + 1) / (2 * (n + 1) * (2 * n + 3)))
        arcsin += a
        n += 1
    return arcsin


comm = MPI.COMM_WORLD

rank = comm.Get_rank()
k = comm.Get_size()  # кол-во запущенных процесов
eps = 0
points_to_share = []

if rank == 0:
    # ввод данных
    A = Decimal(input("input A: "))
    B = Decimal(input("input B: "))
    if A > B:
        c = A
        A = B
        B = c
    if A < -1:
        A = -1
    if B > 1:
        B = 1
    eps = abs(int(input("input eps: ")))
    n = abs(int(input("input n: ")))
    getcontext().prec = eps  # установка точности для точек, которые будут отправлены
    # точки для которых надо рассчитать значение функции
    c = (B - A) / (n - 1)
    points = list(A + c * i for i in range(0, n))

    # массив масивов с точками, которые отправляются другим процессам
    split_list = np.linspace(0, len(points), k, endpoint=False).round(eps)
    split_list = split_list.astype(int).tolist()
    temp = zip(chain([0], split_list), chain(split_list, [None]))
    points_to_share = list(points[i: j] for i, j in temp)[1:]

# отправить данные всем процесам
eps = comm.bcast(eps, root=0)
points_to_share = comm.scatter(points_to_share, root=0)

# установка точности вычислений для всех процессов
getcontext().prec = eps

# вычислить значения функции в точках
data = []
for point in points_to_share:
    data.append((point, my_arcsin(Decimal(point), eps)))

# отправить мастеру
data = comm.gather(data, root=0)

if rank == 0:
    # получение и вывод данных от других процессов
    for i in range(0, k):
        for (point, value) in data[i]:
            print(point, '', value)
