import sys
import os
import datetime
from datetime import timedelta

t2 = timedelta(weeks=0, days=365, hours=0, seconds=0)

begin = str(datetime.date.today() - t2)

dir_base = os.path.abspath('../')
sys.path.append(dir_base)

print(sys.path)

from ticker import Ticker
from matplotlib import pyplot as plt

if __name__ == '__main__':
    tickers = ['^MERV', 'ALUA', 'BMA', 'BBAR', 'BYMA', 'CVH', 'CEPU', 'CRES', 'EDN', 'GGAL', 'VALO', 'SUPV',
               'MIRG', 'PAMP', 'COME', 'TECO2', 'TXAR', 'TRAN', 'TGNO4', 'TGSUD2', 'YPFD', 'TS', 'APBR']

    tickers = ['TEO', 'DESP', 'MELI', 'GLOB', 'BMA', 'BBAR', 'SUPV', 'GGAL', 'TS',
               'TX', 'PAM', 'EDN', 'CEPU', 'YPF', 'PBR', 'TGS', 'LOMA', 'IRS', 'CRESY']

    BA = False

    for ticker in tickers:
        try:
            if BA == True:
                tck = Ticker(ticker + '.BA', begin=begin)
            else:
                tck = Ticker(ticker, begin=begin)

            a, b, c = tck.get_boll()
            tck.get_ma_close()
            tck.get_volume()
            vol = tck.get_volatility(len_ma=20)
            print(ticker, vol.mean())
            print(tck.get_status_ma())
        except Exception as e:
            print(ticker, 'ERROR', e)

    plt.plot(vol)
    plt.show()