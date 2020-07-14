import pickle
import time

class Reader:

    def __init__(self, file_name='data_price'):

        self.file_name = file_name
       
    
        
    def read(self):    
         
        with open('{}.pickle'.format(self.file_name), 'rb') as filename:
            self.list_ = pickle.load(filename)
                
def calc_inverse(val):

    k = list(v.keys())[0] 
    
    comps = k.split('_')

    rel_in = comps.copy()
    rel_in.reverse()
    try:
        val['_'.join(rel_in)] = 1/val[k]
    except Exception as e:
        print('{}'.format(e))

if __name__ == "__main__":
    re = Reader()
    
    re.read()


   
    for e in re.list_:
        time_ = time.ctime(e['time'])

        for v in e['values']:
            calc_inverse(v)

        print(time_)

        for v in e['values']:
           try:
                key = list(v.keys())[0]
                key1 = list(v.keys())[1]
                print('{:>25} {:.8f} {:.8f}'.format(key, v[key], v[key1]))

                if key == 'dai_eth':
                   dai_eth = 0
                   dai_eth = v[key]
                if key == 'dai_zrx':
                   dai_zrx = 0
                   dai_zrx = v[key]

           except Exception as e:
                print('{}'.format(e))


        print('{:>25} {:.8f} {:.8f}'.format('eth_zrx', dai_zrx / dai_eth, dai_eth / dai_zrx))

