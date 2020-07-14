from yahoofinancials import YahooFinancials as YF

having = ['AAPL', 'BA', 'C', 'DIS', 'FB', 'GE', 'GOOGL', 'IBM', 'INTC', 'JPM', 'KO', 'MSFT', 'QCOM', 'T']

tickers = ['CAT', 'NKE', 'AMAT','HON','WFC', 'DE',
           'MCD','PFD', 'AXP', 'MMM', 'MRK', 'TOT', 
           'GLOB','TX', 'TWTR', 'AMZN', 'TSLA','VIST']

tickers_adr = ['TEO',  'SUPV','YPF', 'TX', 'TS',  
               'MELI', 'BMA', 'PAM', 'BBAR', 'GGAL', 
               'EDN', 'PBR', 'DESP']
       
forget = ['TS.BA', 'APBR.BA']      
     
tickers_arg = ['TECO2.BA','YPFD.BA', 'SUPV.BA', 'TXAR.BA', 'BBAR.BA', 
               'MELI.BA', 'BMA.BA', 'PAMP.BA',  'GGAL.BA', 'EDN.BA',  
               'GLNT.BA',  'DESP.BA', 'ALUA.BA']
            
tickers_extra = ['AMD', 'NFLX', 'NVDA', 'WMT', 'PYPL', 
		 'BIDU', 'BABA', 'TCEHY', 'V', 'CSCO', 'SQ',]


semiconductors = ['SWKS', 'XLNX', 'MXIM',  'NXPI', 'TSM', 'QCOM', 
                  'AVGO', 'MU', 'TXN', 'QRVO', 'ON', 'SWKA', 'AMAT', 'LRCX', 
                  'ASX', 'KLAC', 'NATI', 'IMOS', 'MX', 'MXL', 'ADI', 'STM', 'MCHP']
                  
to_consider = ['TSM', 'AMD', 'NFLX', 'NVDA', 'WMT', 'PYPL', 'BIDU', 'BABA', 'TCEHY', 'GLOB', 'V', 'CSCO', 'SQ', 'TXN']

softick = ['VZ', 'SPLK', 'DDOG', 'ESTC', 'MDB', 'OKTA','CRM', 'AYX', 'TWLO', 
            'GLOB', 'NEWR', 'MGNI', 'ZNGA', 'ZS']

def get_number_for_None(number, out_=-99.99):

     if type(number) is str:
         return number
     elif type(number) is float:
         return '{0:.2f}'.format(number) if number != None else out_
     else:
         return str(out_)



def fundamentals(tickers, begin="2020-05-26", end="2020-06-26",):
    format_header = '{:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>10} {:>10}'
    format_numbers = '{:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6} {:>6}  {:>6} {:>10.2e} {:>10.2E}'
    print(format_header.format('ticker', 'P/E', 'EARNSH', 'BK/PR', 'DY', 'DR', 'VAR', 'PEG', 'PS', 'PCI', 'VOLPR', 'CM',))

    for ticker in tickers:
        yf = YF(ticker)

        try:
            pe = get_number_for_None(get_number_for_None(yf.get_pe_ratio()))
            prices = yf.get_historical_price_data(begin, end, "daily")[ticker]['prices']
            stat_pr = calc_statistics(prices)
            var_pr = get_number_for_None(100 * stat_pr[1] / stat_pr[0])
            volume = get_number_for_None(stat_pr[4])
            es = get_number_for_None(yf.get_earnings_per_share())
            sh = get_number_for_None(yf.get_num_shares_outstanding(price_type='current'))
        
            ''' "pegRatio" "priceToBook" "heldPercentInstitutions" '''
            
            statistics = yf.get_key_statistics_data()[ticker]
            summary = yf.get_summary_data()[ticker]
            peg = get_number_for_None(statistics["pegRatio"])
            PCI = get_number_for_None(statistics["heldPercentInstitutions"])
            bv = yf.get_key_statistics_data()[ticker]['bookValue']
            pr = yf.get_current_price()

            if pr is not None and bv is not None:
                pr_bv = get_number_for_None(pr/bv)
            else:
                pr_bv = '-99.99'

            f_s = yf.get_financial_stmts('annual', 'income')['incomeStatementHistory'][ticker][0]
            f_s_key = list(f_s.keys())[0]
            totalRevenue = f_s[f_s_key]['totalRevenue']
            outstanding = statistics["sharesOutstanding"]
            rev_per_share = totalRevenue / outstanding
            
            if pr is not None and es is not None:
                p_s = get_number_for_None(rev_per_share/float(es))
            else:
                p_s = '99'

              
            dy = get_number_for_None(yf.get_dividend_yield())
            dr = get_number_for_None(yf.get_dividend_rate())
        
            volume10days = summary['averageVolume10days']
            marketCap = summary['marketCap']
        
            # float(volume)*pr
            # float(sh)*pr)
            print(format_numbers.format(ticker, pe, es, pr_bv, dy, dr, var_pr, peg, p_s, PCI, volume10days, marketCap))
        except Exception as e:
            print(ticker, e)
        
import statistics as stats

def calc_statistics(prices):
    prs = []
    vols = []
    for pr in prices:
       ave = (pr['high'] + pr['low'] + pr['close'] + pr['open'])/4
       prs.append(ave)
       vols.append(pr['volume'])
    try:
       mean = stats.mean(prs)
       stde = stats.stdev(prs)
       min_ = min(prs)
       max_ = max(prs)
       
       mean_vol = stats.mean(vols)
       stde_vol = stats.stdev(vols)
       min_vol = min(vols)
       max_vol = max(vols)
       
       
       return (mean, stde, min_, max_, mean_vol, stde_vol, min_vol, max_vol)
    except Exception as e:
       return (1, 0, 0, 0, 0, 0, 0)
    




def test_prices():
    ticker = 'BA'
    yf = YF(ticker)
    
    prices = yf.get_historical_price_data("2020-05-26", "2020-06-26", "daily")[ticker]['prices']
    
    print(prices)
    
    print(calc_statistics(prices))
    
from datetime import timedelta
from datetime import datetime

   
def get_fundamentals(tickers, days=90):
    # test_prices()
    delta = timedelta(days=days)
    oggi = datetime.today()
    begin = oggi - delta
    
    print(str(begin).split()[0], str(oggi).split()[0])
   
    fundamentals(tickers, str(begin).split()[0], str(oggi).split()[0])     

def get_string_date(datetime):
    return  str(datetime).split()[0]   
    


def simulation():
    tickers = ['BA', 'DIS', 'KO', 'C', 'GE', 'INTC']

    delta = timedelta(days=90)
    oggi = datetime.today()
    begin = oggi - delta

    prices_dict = dict()
   
    for ticker in tickers:
        yf = YF(ticker)
    
        prices = yf.get_historical_price_data(str(begin).split()[0], str(oggi).split()[0], "daily")[ticker]['prices']
    
        for pr in prices:
           ohlc4 = (pr['high'] + pr['low'] + pr['close'] + pr['open'])/4
           pr['ohlc4'] = ohlc4
        prices_dict[ticker] = prices
    
    print(prices_dict)
    
    date_info = dict()
    for pr in prices_dict:
       print(pr)
       for da in prices_dict[pr]:
           if da['formatted_date'] not in date_info:
               date_info[da['formatted_date']] = dict()
               date_info[da['formatted_date']][pr] = da['ohlc4']
           else:
               date_info[da['formatted_date']][pr] = da['ohlc4']

    # for date in date_info:
    #    print(date)
    #    print(date_info[date])
        
    for ti in date_info['2020-03-30']:
        print(ti, date_info['2020-03-30'][ti])
               
               
    # tc21 tx22 pr13 pr15 
    
if __name__ == '__main__':
    # simulation()
    get_fundamentals(softick)
    
    
