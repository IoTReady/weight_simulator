from random import randint

FNAME = "weights.txt"
NUM = 1000

with open(FNAME, "w") as f:
    for i in range(NUM):
        ok = True
        if randint(1,10) > 8:
            ok = False
        if ok:
            weight = randint(18000,18020)
        else:
            weight = randint(-1500,20000)
        f.write(str(weight)+'\n')