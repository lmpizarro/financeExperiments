import requests
import time

url="https://api.coingecko.com/api/v3/simple/price{}"
url_bitfinex = "https://api-pub.bitfinex.com/v2/tickers?symbols={}"


query = "?ids=havven%2Cethereum%2Cbitcoin%2Cdai&vs_currencies=usd"

uri = url.format(query)

out_format_g = "btc {:.2f} eth {:.2f} dai {:.2f} eth/dai {:.2f} \
eth/btc {:.2f} snx {:.2f} snx/btc {:.2f}"


def update_f(list_l, price):
    del list_l[0]
    list_l.append(price)

def get_ave(list_l):
   av = 0
   for i,p in enumerate(list_l):
      av += p
   return(av/(i+1))

dai_lshort = 20*[0]


while True:
    
    response = requests.get(uri).json()

    snx = response['havven']['usd']

    btc = response['bitcoin']['usd']

    eth = response['ethereum']['usd']

    dai = response['dai']['usd']

    update_f(dai_lshort, eth/dai)

    print(out_format_g.format(btc, eth, dai, eth/dai, btc/eth, snx, btc/snx))

    print('max {:.2f} min {:.2f} ave {:.2f}'.format(max(dai_lshort), min(dai_lshort), get_ave(dai_lshort)))
    
    
    time.sleep(.7)
