import sys
import os
import datetime
from datetime import timedelta

import numpy as np

t2 = timedelta(weeks=0, days=360, hours=0, seconds=0)

begin = str(datetime.date.today() - t2)

dir_base = os.path.abspath('../')
sys.path.append(dir_base)

print(sys.path)

from ticker import Ticker
from matplotlib import pyplot as plt


def test_01():
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

def relation_US_BA(ticker, ticker_ba):
    tck_ba = Ticker(ticker_ba, begin=begin)
    tck = Ticker(ticker, begin=begin)

    tck.get_historical_price_data()
    tck_ba.get_historical_price_data()

    prices = {}
    for price in tck.historical_data['prices']:
        fd = price['formatted_date']
        prices[fd] = price

    prices_ba = {}
    for price in tck_ba.historical_data['prices']:
        fd = price['formatted_date']
        prices_ba[fd] = price

    rel = []
    for pk in prices_ba:
        if pk in prices:
            print({'date': pk, 'price_ba': prices_ba[pk]['adjclose'], 'price': prices[pk]['adjclose']})
            try:
                rel.append(prices[pk]['adjclose']/prices_ba[pk]['adjclose'])
            except Exception as e:
                print(e)


    rel = np.asarray(rel)

    return rel

if __name__ == '__main__':
    tickers = [('BMA','BMA.BA'), ('TS', 'TS.BA'), ('YPF', 'YPFD.BA'), ('GGAL', 'GGAL.BA'), ('BBAR', 'BBAR.BA'), ('PBR', 'APBR.BA')]

    tickers_ = []    # ('BBAR', 'BBAR.BA')]
    tickers_ = [('TS','TEN.MI')]    # ('BBAR', 'BBAR.BA')]
    for tick in tickers:
        rel = relation_US_BA(tick[0], tick[1])
        plt.plot(rel)
        plt.show()

