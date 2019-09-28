import sys
import os
import numpy as np

dir_base = os.path.abspath('../')
sys.path.append(dir_base)

from ticker import Ticker

from matplotlib import pyplot as plt

if __name__ == '__main__':
    tck = Ticker('YPF')
    a, b, c = tck.get_boll()
    tck.get_close()
    tck.get_volume()
    vol = tck.get_volatility()
    tck.get_ma_close()
    print(vol.mean())
    print(tck.get_status_ma())
    vol_osc = tck.get_vol_osc()
    # http://pyhogs.github.io/plot-aspect-ratio.html
    plt.figure(figsize=(12.5, 3))
    plt.bar(np.arange(vol_osc.size), vol_osc)
    plt.plot(vol_osc)
    plt.show()
