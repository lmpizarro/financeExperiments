import os
import sys
import numpy as np

dir_base = os.path.abspath('../')
sys.path.append(dir_base)


from matplotlib import pyplot as plt
from ticker import tickerRT

if __name__ == '__main__':
    ma = tickerRT.Macd()

    s = np.ones(200)
    s[0:50] = 0.0
    s[150:] = 0.0

    close = np.ones(500)
    close[0:50] = 0
    close[50:200] = np.asarray([i/300.0 for i in range(150)])
    close[200:300] = .5
    close[300:500] = np.asarray([0.5 - i/400.0 for i in range(200)])
    close = close + .007*np.random.rand(500)

    macd = np.zeros(500)
    macdSignal = np.zeros(500)
    macdHist = np.zeros(500)

    for i, e in enumerate(close):
        macd[i], macdSignal[i], macdHist[i] = ma.filter(e)
        print(e, ma.filter(e))

    plt.plot(0.030 * close)
    plt.plot(macd)
    plt.plot(macdSignal)
    plt.plot(macdHist)

    plt.show()

