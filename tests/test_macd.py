import sys
import os
import numpy as np

dir_base = os.path.abspath('../')
sys.path.append(dir_base)

from ticker import Ticker

from matplotlib import pyplot as plt

if __name__ == '__main__':

    close = np.ones(500)
    close[0:50] = 0
    close[50:200] = np.asarray([i/300.0 for i in range(150)])
    close[200:300] = .5
    close[300:500] = np.asarray([0.5 - i/400.0 for i in range(200)])

    close = close + .007*np.random.rand(500)

    a,b,c = Ticker.lineal_macd(close)

    plt.figure(figsize=(12.5, 3))
    plt.plot(a[30:])
    plt.plot(b[30:])
    plt.plot(c[30:])
    #plt.show()
    #plt.plot(0.03*close[30:])

    plt.show()

