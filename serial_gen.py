import sys
from time import sleep
from random import randint

import serial

SAMPLES_PER_SECOND =   10
BAUD_RATE = 9600
BYTE_SIZE = serial.SEVENBITS
PARITY = serial.PARITY_EVEN
STOP_BITS = serial.STOPBITS_ONE
STABLE_COUNT = 10

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

            stable_counter += 1
            if stable_counter >= STABLE_COUNT:
                stable_counter = 0

            s = f"W *0      {weight}      0\r\n"
            print(s.strip(), flush=True)
            # 7 data bits can only carry ASCII
            ser.write(s.encode("ascii"))
            sleep(1 / SAMPLES_PER_SECOND)
    except KeyboardInterrupt:
        print("Stopped.", flush=True)
