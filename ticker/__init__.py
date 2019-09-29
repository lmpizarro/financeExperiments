import datetime
import numpy as np
from yahoofinancials import YahooFinancials

from datetime import timedelta

t1 = timedelta(weeks=0, days=1, hours=0, seconds=0)
t2 = timedelta(weeks=0, days=365, hours=0, seconds=0)

begin = str(datetime.date.today() - t2)
end = str(datetime.date.today() - t1)


class Ticker:
    def __init__(self, ticker, begin=begin, end=end):
        self.ticker = ticker
        self.YF = YahooFinancials(ticker)
        self.historical_data = None
        self.historical_price_data = None
        self.begin = begin
        self.end = end

        # https://github.com/JECSand/yahoofinancials
        self.all_statement_data_qt = self.YF.get_financial_stmts('quarterly', ['income', 'cash', 'balance'])


    def get_historical_price_data(self):
        self.historical_data = self.YF.get_historical_price_data(self.begin, self.end, 'daily')[self.ticker]
        self.historical_price_data = self.historical_data['prices']

    def get_close(self):
        if self.historical_data == None:
            self.get_historical_price_data()

        close = np.zeros(len(self.historical_price_data))

        for i, price in enumerate(self.historical_price_data):
            close[i] = (price['high'] + price['open'] + price['close']) / 3.0

        return close

    def get_volume(self):
        if self.historical_data == None:
            self.get_historical_price_data()

        close = np.zeros(len(self.historical_price_data))

        for i, price in enumerate(self.historical_price_data):
            close[i] = price['volume']

        return close

    def get_ma_close(self, len_ma=20):
        close = self.get_close()

        return Ticker.get_ma(close, len_ma)

    def get_ma_volume(self, len_ma=20):
        close = self.get_volume()

        return Ticker.get_ma(close, len_ma)

    @staticmethod
    def get_ma(close, len_ma=20):

        len_close = close.size

        ma_close = np.zeros(len_close)

        if len_close > 2.0 * len_ma:
            for i in range(len_close - len_ma):
                ma_close[i + len_ma] = close[i: i + len_ma].mean()

        return ma_close

    def get_boll(self, len_ma=20):
        close = self.get_close()

        len_close = close.size

        ma_close = np.zeros(len_close)
        std_close = np.zeros(len_close)

        if len_close > 2.0 * len_ma:
            for i in range(len_close - len_ma):
                ma_close[i + len_ma] = close[i: i + len_ma].mean()
                std_close[i + len_ma] = close[i: i + len_ma].std()
        return ma_close + 2 * std_close, ma_close, ma_close - 2 * std_close


    def return_n(self, len_ma=20):
        close = self.get_close()
        len_close = close.size

        ma_close = np.zeros(len_close)

        if len_close > 2.0 * len_ma:
            for i in range(len_close - len_ma):
                ma_close[i + len_ma] = np.log(close[i + len_ma] / close[i])

        return ma_close

    # https://www.wikihow.com/Calculate-Historical-Stock-Volatility
    def get_volatility(self, len_ma=20):
        ret_urn = self.return_n(len_ma)

        mean_return = ret_urn.mean()

        std_return = np.sqrt((ret_urn - mean_return) ** 2 / (ret_urn.size - 1))

        return std_return

    def get_status_ma(self, len_ma=20, short_period=3):

        ma_short = self.get_ma_close(short_period)
        ma_close = self.get_ma_close(len_ma)

        close = ma_short

        criterio = (close[close.size - 1] - ma_close[ma_close.size - 1]) / close[close.size - 1]

        return criterio > 0, criterio < 0, 100 * criterio

    '''
     https://www.investopedia.com/articles/technical/02/082702.asp
     It is important to note that an increasing price, together with declining volume, is always, without exception, 
     bearish. When the market is at the top, one would, therefore, expect to see an oversold volume chart. Another 
     important point: rising volume, together with declining prices, is also bearish.
    '''
    def get_vol_osc(self, len_long=20, len_short=5):
        v_short = self.get_ma_volume(len_short)
        v_long = self.get_ma_volume(len_long)

        return v_short - v_long

    def get_lineal_macd(self, sh=10, lon=20, fil=7):
        close = self.get_close()

        sh_close = self.get_ma(close, sh)
        lon_close = self.get_ma(close, lon)

        macd = sh_close - lon_close

        macd_signal_line = Ticker.get_ma(macd, len_ma=fil)

        macd_hist = macd - macd_signal_line

        return macd_hist, macd_signal_line, macd

    @staticmethod
    def lineal_macd(close, sh=10, lon=20, fil=7):

        sh_close = Ticker.get_ma(close, sh)
        lon_close = Ticker.get_ma(close, lon)

        macd = sh_close - lon_close

        macd_signal_line = Ticker.get_ma(macd, len_ma=fil)

        macd_hist = macd - macd_signal_line

        decay = 0.75

        macd_hist = Ticker.iir(macd_hist, decay)

        return macd_hist, macd_signal_line, macd

    @staticmethod
    def iir(signal, decay):

        b = 1 - decay

        y = np.zeros(signal.size)

        for i in range(1, signal.size):
            y[i] = y[i-1] + b * (signal[i] - y[i-1])
        return y

    # iir low pass filter
    # https://tomroelandts.com/articles/low-pass-single-pole-iir-filter
    @staticmethod
    def lineal_macd_iir(close, sh=.7, lon=.9, fil=.7):
        sh_close = Ticker.iir(close, sh)
        lon_close = Ticker.iir(close, lon)

        macd = sh_close - lon_close

        macd_signal_line = Ticker.iir(macd, fil)

        macd_hist = macd - macd_signal_line

        decay = 0.7

        macd_hist = Ticker.iir(macd_hist, decay)

        return macd_hist, macd_signal_line, macd


class LowPassSinglePole:
    def __init__(self, decay):
        self.b = 1 - decay
        self.reset()

    def reset(self):
        self.y = 0

    def filter(self, x):
        self.y += self.b * (x - self.y)
        return self.y


class Macd:
    def __init__(self, fast=.9, slow=.95, ufast=.85):
        self.fastFilter = LowPassSinglePole(fast)
        self.fastFilter.reset()
        self.slowFilter = LowPassSinglePole(slow)
        self.slowFilter.reset()
        self.Macd_Signal = LowPassSinglePole(ufast)
        self.Macd_Signal.reset()
        self.difference = 0.0

    def reset(self):
        self.Macd_Signal.reset()
        self.slowFilter.reset()
        self.fastFilter.reset()
        self.difference = 0.0
        self.macdSignal = 0.0
        self.macdHist = 0.0

    def filter(self, signal):
        f = self.fastFilter.filter(signal)
        s = self.slowFilter.filter(signal)
        self.difference = f - s
        self.macdSignal = self.Macd_Signal.filter(self.difference)
        self.macdHist = self.difference - self.macdSignal

        return self.difference, self.macdSignal, 5 * self.macdHist


class MaFastSlow:

    def __init__(self, m=5, n=10, thr=1.0):
        if n > m:
            self.n = n
            self.m = m
        else:
            self.m = m
            self.n = m + 1

        self.x_slow = np.zeros(n)
        self.y_fast = np.zeros(m)

        self.thr = thr

    def reset(self):
        self.x_slow = np.zeros(self.n)
        self.y_fast = np.zeros(self.m)

    def filter(self, signal1):


        self.x_slow = np.roll(self.x_slow, 1)
        self.y_fast = np.roll(self.y_fast, 1)
        self.x_slow[0] = signal1
        self.y_fast[0] = signal1

        fast = self.y_fast.mean()
        slow = self.x_slow.mean()
        # print(y_fast, x_slow)

        return (fast - slow) > self.thr

