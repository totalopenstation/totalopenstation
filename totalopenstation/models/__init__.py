# -*- coding: utf-8 -*-
# filename: formats/__init__.py
# Copyright 2008-2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008-2011 Stefano Costa <steko@iosa.it>

# This file is part of Total Open Station.

# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.


import serial
import sys

from time import sleep
from threading import Event, Thread

from totalopenstation.utils.upref import UserPrefs

class Connector(serial.Serial, Thread):
    '''Connect to a total station.

    For more information : `Pyserial documentation <https://pythonhosted.org/pyserial/pyserial_api.html#native-ports>`_

    Args:
        port: Device name or :const:`None`.
        baudrate (int): Baud rate such as 9600 or 115200 etc.
        bytesize: Number of data bits.
        parity: Enable parity checking.
        stopbits: Number of stop bits.
        timeout (float): Set a read timeout value.
        xonxoff (bool): Enable software flow control.
        rtscts (bool): Enable hardware (RTS/CTS) flow control.
        bool dsrdtr (bool): Enable hardware (DSR/DTR) flow control.
        writeTimeout (float): Set a write timeout value.
    '''

    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N',
                stopbits=1, timeout=None, xonxoff=0, rtscts=0,
                writeTimeout=None, dsrdtr=None):

        self.upref = UserPrefs()
        sleeptime = float(self.upref.getvalue('sleeptime'))

        Thread.__init__(self)
        self.dl_started = Event()
        self.dl_finished = Event()

        serial.Serial.__init__(self, port=port, baudrate=baudrate,
        bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout,
        xonxoff=xonxoff, rtscts=rtscts, writeTimeout=writeTimeout,
        dsrdtr=dsrdtr)

    def open(self):
        '''Open the serial link.
        '''

        serial.Serial.open(self)

    def download(self):
        '''Download method for user interfaces.

        First the class must be instantiated, then the port is open and the
        transfer from the device can start. Once the transfer is finished
        the user interface should call this method.'''

        n = self.inWaiting()
        result = self.read(n)

        # looks like there is a maximum buffer of 4096 characters, so we have
        # to wait for a short time and iterate the process until finished

        sleep(sleeptime)

        while self.inWaiting() > 0:
            result = result + self.read(self.inWaiting())
            sleep(sleeptime)

        self.result = result

    def fast_download(self):
        '''Implement a *fast* download method that requires less user input.

        Inside, it calls download() itself, just wrapping it inside another
        loop that checks whether there's input coming from the serial port:
        when data become to appear, download() can start.
        '''

        while self.inWaiting() == 0:
            sleep(sleeptime)
        self.dl_started.set()
        try:
            self.download()
        except threading.exceptions.KeyboardInterrupt:
            sys.exit()
        else:
            self.dl_finished.set()

    def run(self):
        self.fast_download()


BUILTIN_MODELS = {
    'leica_tcr_1205': ('leica_tcr_1205', 'ModelConnector', 'Leica TCR 1205'),
    'zeiss_elta_r55': ('zeiss_elta_r55', 'ModelConnector', 'Zeiss Elta R55'),
    'nikon_npl_350': ('nikon_npl_350', 'ModelConnector','Nikon NPL 350'),
    'leica_tcr_705': ('leica_tcr_705', 'ModelConnector', 'Leica TCR 705'),
    'trimble': ('trimble', 'ModelConnector', 'Trimble'), 
    'topcon_gpt_3005': ('topcon_gpt_3005', 'ModelConnector', 'Topcon GPT 3005'),
    'custom': ('custom', 'CustomConnector', 'Custom/Unknown'),
    }
