import sys
from time import sleep
from random import randint

SAMPLES_PER_SECOND = 10

with open(sys.argv[1], 'w') as f:
    while True:
        ok = True
        if randint(1,10) > 8:
            ok = False
        if ok:
            weight = randint(18000,18020)
        else:
            weight = randint(-1500,20000)
        print(weight)
        f.write(str(weight)+'\r\n')
        sleep(1/SAMPLES_PER_SECOND)
