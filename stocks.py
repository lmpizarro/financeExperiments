from yahoofinancials import YahooFinancials




tickers = ['TEO', 'MELI', 'BMA', 'PAM', 'BBAR', 'GGAL', 'TS', 
           'EDN', 'YPF', 'TX', 'PBR', 'GLOB', 'SUPV', 'DESP']
tickers_arg = ['TECO2.BA', 'MELI.BA', 'BMA.BA', 
               'PAMP.BA', 'BBAR.BA', 'GGAL.BA', 
               'TS.BA', 'EDN.BA', 'YPFD.BA', 'TXAR.BA', 
               'APBR.BA', 'GLNT.BA', 'SUPV.BA', 'DESP.BA']

t_etf = ['GLD', 'USO', 'DBA' ]

tec = ['TWTR', 'AAPL', 'FB', 'AMZN', 'GOOGL', 'MELI', 'GLOB', 'DESP', 'MSFT']

# tickers = tickers_arg

tickers = tickers

keys = ['volume', 'averageVolume', 'averageDailyVolume10Day',
        'open', 'dayHigh', 'dayLow', 'previousClose', 
        'fiftyDayAverage', 'pc_fifty', 'diffVol', 
        'diffVol10', 'diff10Av', 'exDividendDate',]


keys_head = {'volume': 'vol', 'averageVolume': 'averVol', 
             'averageDailyVolume10Day': 'averVol10day',
             'open': 'open', 'dayHigh': 'high', 'dayLow': 'low', 
             'previousClose': 'prevClo', 'fiftyDayAverage': '50dayAver', 
             'pc_fifty': 'pc50', 'diffVol': 'diffVol', 
             'diffVol10': 'diffVol10', 'diff10Av': 'diff10Av', 
             'exDividendDate': 'divDate',}


info_dict = {}

def calc_pc_fifty(summary_ticker, key='fiftyDayAverage'):
    previous = summary_ticker['previousClose']
    fifty = summary_ticker[key]

    try:
        pc = 100.0 * (previous - fifty) / fifty
    except Exception as e:
        pc = None
        print(e)

    summary_ticker['pc_fifty'] = pc


def volume_diff(summary_ticker, limit=100.0):
    volume = summary_ticker['volume']
    avVolu = summary_ticker['averageVolume']
    avVo10 = summary_ticker['averageDailyVolume10Day']
    
    try:
        diff = (volume - avVolu) / avVolu
    except Exception as e:
        diff = 0

    try:
        diff10 = (volume - avVo10) / avVo10
    except Exception as e:
        diff10 = 0

    try:
        diff10Av = (avVo10 - avVolu) / avVolu
    except Exception as e:
        diff10Av = 0


    summary_ticker['diffVol'] = 100 * diff > limit

    summary_ticker['diffVol10'] = 100 * diff10 > limit

    summary_ticker['diff10Av'] = 100 * diff10Av > limit


def set_ticker(summary_ticker, ticker):
    summary_ticker['ticker'] = ticker

if __name__ == '__main__':
    str_out = '      '
    for key in keys:
        str_out += ' ' + keys_head[key]
    print(str_out)
    for ticker in tickers:
        try:
            yf = YahooFinancials(ticker)
            summary = yf.get_summary_data()
            info_dict[ticker] = summary[ticker]
            # fiftyTwoWeekHigh
            calc_pc_fifty(summary[ticker], 'fiftyTwoWeekHigh')
            volume_diff(summary[ticker])
            str_out = ticker
            for key in keys:
                try:
                    resp = summary[ticker][key]
                    if resp == True or resp == False:
                        str_out += ' ' + "{}".format(resp)
                    else: 
                        str_out += ' ' + "{0:.1f}".format(resp)
                except Exception as e:
                    str_out += ' ' + "{:12.12}".format(resp)

            print(str_out)
        except Exception as e:
            print(e)

    try:
        pass
        # print(summary[ticker].keys())
    except Exception as e:
        print(e)


        
    # print(info_dict)

