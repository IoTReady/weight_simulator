import sys
from time import sleep
from random import randint

SAMPLES_PER_SECOND = 10

with open(sys.argv[1], "w") as f:
    while True:
        ok = True
        if randint(1, 10) > 8:
            ok = False
        if ok:
            weight = randint(2400, 2800)
        else:
            weight = randint(-1500, 2000)
        s = f"W *0      {weight}      0\r\n"
        print(s)
        # f.write(str(weight) + "\r\n")
        f.write(s)
        sleep(1 / SAMPLES_PER_SECOND)
