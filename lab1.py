from mpi4py import MPI
import numpy as np

# 16. Рассматривая Х как множество (значения вектора не должны повторяться), найти
# симметрическую разность объединений (X,UX,U…UXL2) (Xle+ U…UX) (где к- количество запущенных
# процессов). Каждый процесс передает свои значения нулевому, который находит симметрическую
# разность объединений и выводит результат.

communication = MPI.COMM_WORLD
rank = communication.rank
size = communication.size
master = 0
tag = 100

if rank == master:
    status = MPI.Status()
    total = []
    a = set()
    b = set()
    # получение результатов
    for i in range(1, size):
        rcv = communication.recv(source=MPI.ANY_SOURCE, tag=tag, status=status)
        print("master: recv value: ", rcv)
        total.append(rcv)
    for i in range(size // 2):
        a = a.union(total[i])
        b = b.union(total[-(i + 1)])
    print("result = ", a ^ b)
else:
    status = MPI.Status()
    d = set(map(lambda x: round(x * 10), np.random.rand(5)))
    print("worker ", rank, "send ", d)
    communication.send(d, dest=master, tag=tag)
