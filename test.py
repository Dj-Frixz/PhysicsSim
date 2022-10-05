from multiprocessing import Process
from time import time,sleep

class Bruh():
    def __init__(self, bruh) -> None:
        self.bruh = bruh

def f1(obj):
    k = time()
    while time()-k<15:
        obj.bruh += 1

if __name__=='__main__':
    j = Bruh(0)
    p1 = Process(target=f1, args=(j,))
    p1.start()
    for i in range(15):
        print(i,j.bruh,sep=' ')
        sleep(1)
    print('waiting...')
    p1.join()
    p1.close()
    print(j.bruh)