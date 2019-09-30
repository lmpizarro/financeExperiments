import numpy as np

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
