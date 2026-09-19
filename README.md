`file_gen.py` - Generate weights and save on new lines to a file.
`file_parse.py` - Parse weights from a file.
`serial_gen.py` - Generate weights and send via serial to simulate a weighing scale.


# Usage:

`python3 serial_gen.py /dev/ttyUSB0`

Serial settings: 9600 baud, 7 data bits, even parity, 1 stop bit (7E1).

Frame format (Toledo continuous output, 17 bytes, ~15 frames/s):

```
STX  SWA  SWB  SWC  WEIGHT(6)  TARE(6)  CR
02   '*'  '0'  ' '  '    90'   '     0' 0D
```

`SWB` is `'0'` when stable, `'8'` in motion, `'2'`/`':'` for negative stable/in motion.
