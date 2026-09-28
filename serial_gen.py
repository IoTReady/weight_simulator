import argparse
from time import sleep
from random import randint

import serial

# Emulates a scale on RS232 @ 9600 baud, 7E1 or 8N1 (--uart).
# Formats:
#   simple:  "+0.345\r"            — sign + decimal kg, 3 dp
#   spec:    "+001.100kg\r"        — sign + 3-digit zero-padded integer + 3 dp + "kg"
#   toledo:  "W *0      500      0\r\n"
#   toledo-continuous: 17-byte Toledo continuous frame (weight in grams)
#       STX  SWA  SWB  SWC  WEIGHT(6)  TARE(6)  CR
#       02   '*'  '0'  ' '  '   500'   '     0' 0D
#     SWB is '0' when stable, '8' in motion, '2'/':' for negative stable/in motion.

BAUD_RATE = 9600
UART_CONFIGS = {
    '7E1': dict(bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE),
    '8N1': dict(bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE),
}
SAMPLES_PER_SECOND = 10
STABLE_REPEATS = 16  # stable frames sent for each weight
MOTION_COUNT = 10  # toledo-continuous: extra "in motion" frames sent before the stable ones

# Toledo continuous output status words
STX = '\x02'
SWA = '*'             # no decimal point, x1 increment
SWB_BASE = 0x30       # gross, positive, kg -> '0'
SWB_NEGATIVE = 0x02
SWB_MOTION = 0x08     # -> '8'
SWC = ' '             # units as selected in SWB
TARE = 0

parser = argparse.ArgumentParser(description='Continuous serial weight simulator.')
parser.add_argument('port', help='Serial port to send weights to, e.g. /dev/ttyUSB0.')
parser.add_argument('--format', choices=['simple', 'spec', 'toledo', 'toledo-continuous'],
                    default='simple', help='Output format (default: simple).')
parser.add_argument('--uart', choices=list(UART_CONFIGS), default='7E1',
                    help=f'UART framing at {BAUD_RATE} baud (default: 7E1).')
args = parser.parse_args()

if args.format == 'spec':
    def encode(grams, in_motion):
        return f'{grams / 1000:+08.3f}kg\r'
elif args.format == 'toledo':
    def encode(grams, in_motion):
        return f'W *0      {grams}      0\r\n'
elif args.format == 'toledo-continuous':
    def encode(grams, in_motion):
        swb = SWB_BASE
        if grams < 0:
            swb |= SWB_NEGATIVE
        if in_motion:
            swb |= SWB_MOTION
        return f'{STX}{SWA}{chr(swb)}{SWC}{abs(grams):>6}{TARE:>6}\r'
else:
    def encode(grams, in_motion):
        return f'{grams / 1000:+.3f}\r'


motion_frames = MOTION_COUNT if args.format == 'toledo-continuous' else 0

with serial.Serial(args.port, BAUD_RATE, **UART_CONFIGS[args.uart]) as f:
    while True:
        ok = randint(1, 10) <= 8
        if ok:
            grams = randint(480, 520)
        else:
            grams = randint(-1500, 20000)
        for i in range(motion_frames + STABLE_REPEATS):
            line = encode(grams, in_motion=i < motion_frames)
            print(repr(line))
            # 7 data bits can only carry ASCII
            f.write(line.encode('ascii'))
            f.flush()
            sleep(1 / SAMPLES_PER_SECOND)
