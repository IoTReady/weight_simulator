`serial_gen.py` - Generate weights and send via serial to simulate a weighing scale.


# Usage:

`python3 serial_gen.py /dev/ttyUSB0 [--format simple|spec|toledo|toledo-continuous] [--uart 7E1|8N1]`

Serial settings: 9600 baud, 7E1 by default, or 8N1 with `--uart 8N1`.
