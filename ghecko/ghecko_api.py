import tkinter
import datetime
import requests
import time

url="https://api.coingecko.com/api/v3/simple/price{}"

import math
sign = lambda x: math.copysign(1, x) # two will work

class ListValues:

    def __init__(self, N, init_val=0):
        self.list_v = N*[init_val]

    def update(self, price):
        del self.list_v[0]
        self.list_v.append(price)

    def average(self):
       av = 0
       for i,p in enumerate(self.list_v):
          av += p
       return(av/(i+1))

    def min(self):
        return min(self.list_v)
    
    def max(self):
        return max(self.list_v)



class CryptoItem:

    map__ = {"havven": "snx", 
             "ethereum": "eth", 
             "bitcoin": "btc", 
             "dai": "dai",
             "augur": "rep",
             "0x": "zrx",
             "wrapped-bitcoin": "wbtc",
             "chainlink": "link",
             "basic-attention-token": "bat"
              }
              
    inverse_map = {v: k for k, v in map__.items()}

    def __init__(self, name):
        self.name = name
        self.symbol = self.map__[name]
        self.value_list = ListValues(20)
        self.value = 0
   
    def get_name(self):
        return self.name

    def get_symbol(self):
        return self.symbol
        
    def set_value(self, value):
        self.value = value
        self.value_list.update(value)

    def __str__(self):
        return self.name
        
    def get_value(self):
        return self.value

import requests
class Prices:
    def __init__(self, names):
       self.names = names
       self.dict_items = {name: CryptoItem(name) for name in names}
       self.query = '?ids={}&vs_currencies=usd'.format('%2C'.join([str(ci) for ci in self.dict_items]))       
       self.uri = url.format(self.query)
       
    def get_uri(self):
        return self.uri
        
    def set_prices(self):
        try:
            response = requests.get(self.uri).json()
            for name in self.dict_items:
                self.dict_items[name].set_value(response[name]['usd'])
                
            
        except Exception as e:
            print(e)

    def get_prices(self):
       data = {self.dict_items[name].symbol: {'price': self.dict_items[name].value,
                                              'max':self.dict_items[name].value_list.max(),
                                              'average':self.dict_items[name].value_list.average(),
                                              'min':self.dict_items[name].value_list.min()} for name in self.dict_items}
       return data
       
    
    def get_name(self, symbol):
        inverse_map = CryptoItem.inverse_map
        
        return inverse_map[symbol]
        
        
    def get_pair(self, pair_symbol):
        name_1 = self.get_name(pair_symbol[0])
        name_2 = self.get_name(pair_symbol[1])
        
        return (self.dict_items[name_1], self.dict_items[name_2])
       


#  pairs=[('dai', 'eth'), ('eth', 'btc'), ('snx', 'btc')]
class PriceRelation:
    def __init__(self, crypto_items):
        self.value_list = ListValues(20)
        self.value = 0
        self.crypto_item1 = crypto_items[0]
        self.crypto_item2 = crypto_items[1]
        self.name = '{}_{}'.format(self.crypto_item2.get_symbol(), self.crypto_item1.get_symbol()) 
        
             
    def set_value(self):
       try:
           self.value = self.crypto_item1.get_value() / self.crypto_item2.get_value()
       except Exception as e:
          print(e)
          self.value = 0
          
       self.value_list.update(self.value)   
        
    def get_value(self):
        return self.value
        
    def __str__(self):
        return 'crypto 1 {} crypto 2 {}'.format(self.crypto_item1.get_name(), self.crypto_item1.get_name())

    def get_name(self):
        return self.name


class PricesRelations:
    def __init__(self, pairs):
        self.price_rels = [PriceRelation(prices.get_pair(pair)) for pair in pairs]
        
    def set_values(self):
        for pr in self.price_rels:
            pr.set_value()
            
    def print_values(self):
        for pr in self.price_rels:
            print('{:>25} {:.8f}'.format(pr.get_name(), pr.get_value()))

    def get_values(self):
        
        return [{pr.get_name(): pr.get_value()} for pr in self.price_rels]

import pickle
class Saver:

    def __init__(self, file_name='data_price', create=True):

        self.file_name = file_name
       
        list_ = []
        
        if create == True:
            with open('{}.pickle'.format(self.file_name), 'wb') as fp:
                pickle.dump(list_, fp)
            
    def add(self, data):
        with open('{}.pickle'.format(self.file_name), 'rb') as filename:
            list_ = pickle.load(filename)
            
            list_.append(data)
        
        with open('{}.pickle'.format(self.file_name), 'wb') as filename:
            list_ = pickle.dump(list_, filename)
            
    
import time
  
if __name__ == "__main__":

    sv = Saver(create=False)
    
    names = ["havven", "ethereum", "bitcoin", "dai", 'augur', 'chainlink', '0x', 'basic-attention-token']

    prices = Prices(names)
    
    pairs=[('eth', 'dai'), ('btc', 'eth'), ('snx', 'eth'), 
            ('rep', 'eth'), ('link', 'eth'), ('snx', 'dai'), 
            ('rep', 'dai'), ('zrx', 'dai'), ('link', 'dai'), ('bat', 'dai')]
    
    relations = PricesRelations(pairs)
    
    
    while True:
        in_time = time.time()
        prices.set_prices()
        relations.set_values()
    
        p = prices.get_prices()
        
        relations.print_values()
        data = relations.get_values()
        data = {'time': time.time(), 'values': data}
        sv.add(data)

        
        print(datetime.datetime.now())
        print()
        
        out_time = time.time()

        sleep_time = 60-(out_time-in_time)
        
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            time.sleep(60)


