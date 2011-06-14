#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: generic.py

import serial
import sys

from time import sleep
from threading import Event, Thread


class Connector(serial.Serial, Thread):

    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N',
                stopbits=1, timeout=None, xonxoff=0, rtscts=0,
                writeTimeout=None, dsrdtr=None):

        Thread.__init__(self)
        self.dl_started = Event()
        self.dl_finished = Event()

        serial.Serial.__init__(self, port=port, baudrate=baudrate,
        bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout,
        xonxoff=xonxoff, rtscts=rtscts, writeTimeout=writeTimeout,
        dsrdtr=dsrdtr)

    def open(self):
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

        sleep(0.1)

        while self.inWaiting() > 0:
            result = result + self.read(self.inWaiting())
            sleep(0.3) # TODO determine sleep time from baudrate

        self.result = result

    def fast_download(self):
        '''Implement a `fast' download method that requires less user input.

        Inside, it calls download() itself, just wrapping it inside another
        loop that checks whether there's input coming from the serial port:
        when data become to appear, download() can start.
        '''

        while self.inWaiting() == 0:
            sleep(0.1)
        self.dl_started.set()
        try:
            self.download()
        except threading.exceptions.KeyboardInterrupt:
            sys.exit()
        else:
            self.dl_finished.set()

    def run(self):
        self.fast_download()
