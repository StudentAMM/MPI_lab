# mpiexec -n 4 python lab4.py
# создать описатель типа и использовать его при передаче данных в качестве шаблона
# для следующего преобразования

# 7 верхний левый треугольник

from mpi4py import MPI
import random

SIZE = 4


class My(object):

    def __init__(self):
        self.x = [[random.randrange(0, 15) for y in range(SIZE)] for x in range(SIZE)]

    def __getstate__(self):
        return {'special_x': self.x}

    def __setstate__(self, state):
        # state — то, что вернулось из __getstate__
        temp = state['special_x']
        res = []
        for i in range(0, SIZE):
            for j in range(0, SIZE - i):
                res.append(temp[i][j])

        self.x = res


comm = MPI.COMM_WORLD
size = comm.size
rank = comm.rank
master = 0
tag = 100

if rank == master:
    # получение результатов
    for i in range(1, size):
        rcv = comm.recv(source=MPI.ANY_SOURCE, tag=tag)
        print(rcv.x)
else:
    d = My()
    print(d.x)
    comm.send(d, dest=master, tag=tag)
