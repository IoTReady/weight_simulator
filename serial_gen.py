import sys
from time import sleep
from random import randint

import serial

SAMPLES_PER_SECOND = 15
BAUD_RATE = 9600
BYTE_SIZE = serial.SEVENBITS
PARITY = serial.PARITY_EVEN
STOP_BITS = serial.STOPBITS_ONE
STABLE_COUNT = 10
MOTION_COUNT = 3  # frames flagged "in motion" after each weight change

# Toledo continuous output (17 bytes):
#   STX, status words A/B/C, weight (6, right-aligned), tare (6), CR
STX = "\x02"
SWA = "*"             # no decimal point, x1 increment
SWB_BASE = 0x30       # gross, positive, kg -> '0'
SWB_NEGATIVE = 0x02
SWB_MOTION = 0x08     # -> '8'
SWC = " "             # units as selected in SWB
TARE = 0


def toledo_frame(weight, in_motion):
    swb = SWB_BASE
    if weight < 0:
        swb |= SWB_NEGATIVE
    if in_motion:
        swb |= SWB_MOTION
    return f"{STX}{SWA}{chr(swb)}{SWC}{abs(weight):>6}{TARE:>6}\r"


if len(sys.argv) < 2:
    sys.exit(f"Usage: {sys.argv[0]} <serial-port>    e.g. {sys.argv[0]} /dev/ttyUSB0")

with serial.Serial(sys.argv[1], baudrate=BAUD_RATE, bytesize=BYTE_SIZE,
                   parity=PARITY, stopbits=STOP_BITS) as ser:
    stable_counter = 0
    weight = None
    try:
        while True:
            if stable_counter == 0:
                ok = True
                if randint(1, 10) > 8:
                    ok = False
                if ok:
                    weight = randint(2400, 2800)
                else:
                    weight = randint(-1500, 2000)

            in_motion = stable_counter < MOTION_COUNT
            stable_counter += 1
            if stable_counter >= STABLE_COUNT:
                stable_counter = 0

            s = toledo_frame(weight, in_motion)
            print(repr(s), flush=True)
            # 7 data bits can only carry ASCII
            ser.write(s.encode("ascii"))
            sleep(1 / SAMPLES_PER_SECOND)
    except KeyboardInterrupt:
        print("Stopped.", flush=True)
