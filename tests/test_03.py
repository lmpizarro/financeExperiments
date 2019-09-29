import numpy as np
import os
import sys
import itertools
import time


dir_base = os.path.abspath('../')
sys.path.append(dir_base)

from ticker import MaFastSlow

if __name__ == '__main__':

    fs = MaFastSlow()

    s = np.ones(10)
    s = np.asarray(
        [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
         15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15,15,15,15,
         14, 13, 12, 11, 10, 9, 8, 7, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    gen = itertools.cycle(s)


    N = 0
    while True:
        time.sleep(1)

        n = gen.__next__()
        noise = np.random.normal(0, n*.01, 1)
        n = n + noise[0]

        out_filter = fs.filter(signal1=n)


        print(N, n, out_filter)

        N = N + 1
