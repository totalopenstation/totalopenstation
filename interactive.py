#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: interactive.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import serial

from time import sleep

ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, bytesize=serial.SEVENBITS, timeout=0, parity=serial.PARITY_NONE, rtscts=1)
ser.open()

# start from the device...
a = raw_input("Digit something and press ENTER when download has finished\n")
# wait until finished!

n = ser.inWaiting()
result = ser.read(n)

# looks like there is a maximum buffer of 4096 characters, so we have to
# wait and iterate the process until finished

sleep(7)

while ser.inWaiting() > 0:
    result = result + ser.read(ser.inWaiting())
    sleep(7)
print(result)

e = open('interactive_download.txt', 'w')

e.write(result)
e.close()

