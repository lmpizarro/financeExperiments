import sys


val_ma_cal = 30*[0]

def update_f(list_l, price):
    del list_l[0]
    list_l.append(price)

def get_ave(list_l):
   av = 0
   for i,p in enumerate(list_l):
      av += p
   return(av/(i+1))


if __name__ == '__main__':
    val = []
    inver = []
    aver = []
    
    for line in sys.stdin:
        line = [float(e) for e in line.split()[1:]]
        # sys.stdout.write(line)
        val.append(line[0])
        inver.append(line[1])
        update_f(val_ma_cal, line[0])
        aver.append(get_ave(val_ma_cal))
    for a,v in zip(val,aver):
        print(a,v)


