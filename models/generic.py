#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: generic.py

import serial

from time import sleep

class Connector(serial.Serial):
    def __init__(self, port=None, baudrate=9600, bytesize=8, parity='N',
                stopbits=1, timeout=None, xonxoff=0, rtscts=0,
                writeTimeout=None, dsrdtr=None):
        
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
        self.downloaded = False
    
        # looks like there is a maximum buffer of 4096 characters, so we have
        # to wait for a short time and iterate the process until finished
        
        sleep(0.1)
        
        while self.inWaiting() > 0:
            result = result + self.read(self.inWaiting())
            sleep(0.3) # TODO find some clever way to determine sleep time from baudrate
        
        self.result = result
        return self.result
    
    def fast_download(self):
        '''Implement a `fast' download method that requires less user input.
        
        Inside, it calls download() itself, just wrapping it inside another
        loop that checks whether there's input coming from the serial port:
        when data become to appear, download() can start.
        '''
        
        # TODO printing from within the library method is UGLY™
        # An event system should be able to catch signals from the running process
        
        while self.inWaiting() == 0:
            sleep(0.1)
        print "\nStarting download\n"
        self.download()
        print "Download finished\n"
        return self.result


class Point:
    
    def __init__(self, p_id, x, y, z, text):
        
        self.p_id= p_id
        self.x=x
        self.y=y
        self.z=z
        self.text=text
        
        self.tuplepoint = (self.p_id, self.x, self.y, self.z, self.text)
    
    def __str__(self):
        return self.p_id, self.x, self.y, self.z, self.text


class Parser:
    '''Parses a *single* string of raw data and turns it to the internal format.
    
    This means that if you plan to load data from a file you have to pass
    the output of open(file).read() to this class.'''
    
    def __init__(self, data, swapXY=False):
        
        self.d = data.splitlines()
        self.swapXY = swapXY
        
        valid_lines = filter(self.is_point, self.d)
        fg_lines = map(self.get_point, valid_lines)
        self.points = [ p.tuplepoint for p in fg_lines if p is not None ]
    
    def is_point(self):
        pass
    
    def get_point(self):
        pass

