# mpiexec -n 4 python lab3.py
# Задание 3
# Каждый процесс заполняет свой массив размером п случайными
# числами. Для решения задачи использовать операции приведения с
# собственной функцией для решения задачи, Результат вектор размером n,
# каждый элемент которого получен по правилу определенной в задаче
# функции (найти количество четных)

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank

array_size = 10


def myadd(xmem, ymem, dt):
    x = np.frombuffer(xmem, dtype=np.int)
    y = np.frombuffer(ymem, dtype=np.int)

    z = x + y

    # print("Rank %d reducing %s (%s) and %s (%s), yielding %s" % (rank, x, type(x), y, type(y), z))

    y[:] = z


# создание собственного оператора/функции
op = MPI.Op.Create(myadd, commute=True)

recvdata = np.zeros(array_size, dtype=np.int)
# случайный массив целых чисел
temp = np.random.randint(0, 10, array_size)
print(rank, temp)
temp2 = temp % 2 == 0
print(temp2)
senddata = temp2.astype(np.int)

print(" process %s sending %s " % (rank, senddata))

comm.Reduce(senddata, recvdata, root=0, op=op)

if rank == 0:
    print('on task', rank, 'after Reduce:    data = ', recvdata)
