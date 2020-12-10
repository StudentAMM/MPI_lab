# mpiexec -n 4 python lab5.py
# Даны две матрицы размером n*n (n количество запущенных про-
# цессов). Матрицы распределены между процессами. Каждый процесс ге-
# нерирует строку матрицы А и строку (или столбец) матрицы В. Память
# отводится только для строки А и строки (столбца) В. Для вычисления по
# формуле процесс использует свою строку матрицы А, а строки (столбцы)
# матрицы В передаются последовательно каждому процессу, при этом ис-
# пользуется виртуальная топология «кольцо». Результат
# каждый процесс вычисляет одно значение и либо выводит его сам, либо передает
# «мастеру», который выводит все.

# 16 res=minSum(aik+bjk)

from mpi4py import MPI
import random
import numpy as np

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
master = 0
tag = 100

SIZE = 3

left = rank - 1
if left == -1:
    left = size - 1
right = (rank + 1) % size

A = [random.randrange(0, 15) for y in range(SIZE)]
# print("I'm myrank {0}: A {1}".format(rank, A))
B = [random.randrange(0, 15) for y in range(SIZE)]
# print("I'm myrank {0}: B {1}".format(rank, B))
C = [np.sum(A)+np.sum(B)]
msg_recv = B
# идем до size-1 т.к на первом шаге наш поцесс уже совершил обработку
for i in range(0, size - 1):
    # отправка
    comm.send(msg_recv, dest=right, tag=tag)
    print("I'm myrank {0}: send {1} to processor {2}".format(rank, msg_recv, right))
    # получение результатов
    rcv = comm.recv(source=MPI.ANY_SOURCE, tag=tag)
    # print("I'm myrank {0}: received {1} from {2}".format(rank, rcv, left))
    msg_recv = rcv
    C.append(np.sum(A)+np.sum(rcv))
print('temp sum: ', C)
print(np.min(C))
