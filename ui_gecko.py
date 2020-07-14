import tkinter
import datetime
import requests

url="https://api.coingecko.com/api/v3/simple/price{}"
names = ["havven", "ethereum", "bitcoin", "dai"]

import math
sign = lambda x: math.copysign(1, x) # two will work

class ListValues:

    def __init__(self, N, init_val=0):
        self.list_v = N*[init_val]

    def update_f(self, price):
        del list_v[0]
        list_v.append(price)

    def get_ave(self):
       av = 0
       for i,p in enumerate(self.list_v):
          av += p
       return(av/(i+1))

    def min(self):
        return min(self.list_v)
    
    def max(self):
        return min(self.list_v)



class CryptoItem:

    map__ = {"havven": "snx", "ethereum": "eth", "bitcoin": "btc", "dai": "dai"}

    def __init__(self, name):
        self.name = name
        self.symbol = self.map__[name]
        self.value_list = 20*[0]

   
    def get_name(self):
        return self.name


    def __str__(self):
        return self.name


ci_l = [CryptoItem(name) for name in names]

query = '?ids={}&vs_currencies=usd'.format('%2C'.join([str(ci) for ci in ci_l]))

uri = url.format(query)


def get_prices():
    response = requests.get(uri).json()

    try:
        snx = response['havven']['usd']
        btc = response['bitcoin']['usd']
        eth = response['ethereum']['usd']
        dai = response['dai']['usd']
    except Exception as e:
        print(e)

    return (btc, eth, snx, dai)

def update_f(list_l, price):
    del list_l[0]
    list_l.append(price)

def get_ave(list_l):
   av = 0
   for i,p in enumerate(list_l):
      av += p
   return(av/(i+1))

dai_list = 20*[0]
btc_list = 20*[0]
eth_list = 20*[0]
snx_list = 20*[0]
eth_dai_list = 20*[0]
btc_eth_list = 20*[0]
snx_btc_list = 20*[0]


root = tkinter.Tk()
text_header = "btc           eth           snx        dai    eth/dai    eth/btc       snx/btc"

lab_header = tkinter.Label(root)
lab_header.pack()

lab_prices = tkinter.Label(root)
lab_prices.pack()

lab_max = tkinter.Label(root)
lab_max.pack()

lab_ave = tkinter.Label(root)
lab_ave.pack()

lab_min = tkinter.Label(root)
lab_min.pack()


# frame = tkinter.Frame()
# frame.pack(side=tkinter.LEFT)

lab_header.config(text=text_header)


format_g = "{:.2f}    {:.2f}    {:.2f}     {:.2f}    {:.2f}   {:.2f}       {:.2f}"
format_g2 = "{:.2f}    {:.2f}    {:.2f}     {:.2f}                                "



lab_time = tkinter.Label(root)
lab_time.pack()

def get_res(list_):
    
    return (min(list_), max(list_), get_ave(list_))

# dai_trend = eth_trend = snx_trend = btc_trend = btc_eth_trend = 0 
def clock():
    global dai_trend, eth_trend, snx_trend, btc_trend
    
    time = datetime.datetime.now().strftime("Time: %H:%M:%S")

    (btc, eth, snx, dai) = get_prices()
    
    snx_btc = float(btc) / float(snx)
    eth_dai = float(eth) / float(dai)
    btc_eth = float(btc) / float(eth)

    update_f(dai_list, dai)
    update_f(btc_list, btc)
    update_f(btc_eth_list, btc_eth)
    update_f(eth_list, eth)
    update_f(eth_dai_list, eth_dai)
    update_f(snx_list, snx)
    update_f(snx_btc_list, snx_btc)

    
    min_dai, max_dai, ave_dai = get_res(dai_list)
    min_btc, max_btc, ave_btc = get_res(btc_list)
    min_eth, max_eth, ave_eth = get_res(eth_list)
    min_snx, max_snx, ave_snx = get_res(snx_list)
    
    min_btc_eth, max_btc_eth, ave_btc_eth = get_res(btc_eth_list)
    min_eth_dai, max_eth_dai, ave_eth_dai = get_res(eth_dai_list)
    min_snx_btc, max_snx_btc, ave_snx_btc = get_res(snx_btc_list)
    
    dai_trend = sign(dai - ave_dai)
    snx_trend = sign(snx - ave_snx)
    btc_trend = sign(btc - ave_btc)
    eth_trend = sign(eth - ave_eth)
    
    btc_eth_trend = sign(btc_eth - ave_btc_eth)
    eth_dai_trend = sign(eth_dai - ave_eth_dai)
    snx_btc_trend = sign(snx_btc - ave_snx_btc)

   
    print(format_g.format(btc_trend, eth_trend, snx_trend, dai_trend, eth_dai_trend, btc_eth_trend, snx_btc_trend))
    
    text_prices = format_g.format(btc, eth, snx, dai, eth_dai, btc_eth, snx_btc)
    lab_prices.config(text=text_prices)
    lab_max.config(text=format_g.format(max_btc, max_eth, max_snx, max_dai, max_eth_dai, max_btc_eth, max_snx_btc))   
    lab_min.config(text=format_g.format(min_btc, min_eth, min_snx, min_dai, min_eth_dai,  min_btc_eth,  min_snx_btc))   
    lab_ave.config(text=format_g.format(ave_btc, ave_eth, ave_snx, ave_dai, ave_eth_dai, ave_btc_eth, ave_snx_btc))    

    lab_time.config(text=time)
    
    root.after(5000, clock) # run itself again after 1000 ms



# run first time
clock()

root.mainloop()
