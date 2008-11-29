#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: interactive.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from models import *


station = zeiss_elta_r55.ModelConnector('/dev/ttyUSB0')
station.open()

# start from the device...
a = raw_input("Press ENTER when download has finished\n")
# wait until finished!

result = station.download()
print result

e = open('interactive_download.txt', 'w')
e.write(result)
e.close()

