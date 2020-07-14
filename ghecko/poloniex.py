import time
import requests

# curl "https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1546300800&end=1546646400&period=14400"

url = "https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}"

period = 3600
end = int(time.time())
start = end - period * 10
pair = "DAI_ETH"

uri = url.format(pair, start, end, period)

data = requests.get(uri).json()

for n,d in enumerate(data):
   print(d)
   
print(n)




