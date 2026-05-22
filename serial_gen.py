import argparse
from time import sleep
from random import randint

# Emulates a scale on RS232 @ 9600 8N1.
# Formats (terminated with CR):
#   simple: "+0.345\r"     — sign + decimal kg, 3 dp
#   spec:   "+001.100kg\r" — sign + 3-digit zero-padded integer + 3 dp + "kg"

SAMPLES_PER_SECOND = 10
REPEATS_PER_WEIGHT = 10

parser = argparse.ArgumentParser(description='Continuous serial weight simulator.')
parser.add_argument('output', help='File or device to write weight strings to.')
parser.add_argument('--format', choices=['simple', 'spec'], default='simple',
                    help='Output format (default: simple).')
args = parser.parse_args()

if args.format == 'spec':
    def encode(grams):
        return f'{grams / 1000:+08.3f}kg\r'
else:
    def encode(grams):
        return f'{grams / 1000:+.3f}\r'

with open(args.output, 'w') as f:
    while True:
        ok = randint(1, 10) <= 8
        if ok:
            grams = randint(480, 520)
        else:
            grams = randint(-1500, 20000)
        line = encode(grams)
        for _ in range(REPEATS_PER_WEIGHT):
            print(line, end='')
            f.write(line)
            f.flush()
            sleep(1 / SAMPLES_PER_SECOND)
