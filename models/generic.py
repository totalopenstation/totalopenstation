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
            sleep(0.1)
        
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
        
        
    def get_coords(self):
        
        coords = {'x': self.x,'y':self.y,'z':self.z}
        return coords
    
    def get_string_of_points(self):
        
        string = str(self.p_id)+" "+str(self.x)+" "+str(self.y)+" "+str(self.z)+" "+str(self.text)
        return string
    
    def dump_point(self):
        
        print self.p_id," ",self.x," ",self.y," ",self.z," ",self.text
    
    def point_to_tuple(self):
        tuplepoint = (self.p_id, self.x, self.y, self.z, self.text)
        return tuplepoint
    
    #def SwapXY(self):
        
        #temp = self.x
        #self.x =self.y
        #self.y=temp

class PointsList:
    
    def __init__(self):
        
        self.listofpoints = []
        
    def add_point(self, p):
        
        self.listofpoints.append(p)
        
    def add_points(self, lp):
        
        self.listofpoints.extend(lp)
        
    def pid_is_in_lop(self, aux_p_id):
        
        for p in self.listofpoints:
            
            if aux_p_id == p.p_id :
                return True
        
        return False
        
    def points_number(self):
        
        return len(self.listofpoints)
        
    def list_to_tuple(self):
        
        list_aux=[]
        for p in self.listofpoints:
            list_aux.append(p.tuplepoint)
        return list_aux

#class Data:
    
    #def __init__(self):
        #pass
        
    #def data_from_txt_file(self, filepathname):
        
        #file = open(filepathname,'r')
        #self.lines = file.readlines()
        #file.close()


class Parser:
    '''Parses a *single* string of raw data and turns it to the internal format.
    
    This means that if you plan to load data from a file you have to pass
    the output of open(file).read() to this class.'''
    ''' WHO THE FUCK ARE THE ARTIC MONKEYS!?!?!?!'''
    ''' This should be a good reason to use the commented class DATA!'''
    
    def __init__(self, data, swapXY=False):
        
        self.d = data.splitlines()
        self.points = PointsList()
        self.swapXY = swapXY
        
        self.parse_retrieve_data()
        
        if self.points.points_number() > 0:
            self.t_points = self.points.list_to_tuple()
        
    def set_data(self, data):
        
        self.d = data
    
    def get_data(self):
        
        return self.d
    
    def parse_retrieve_data(self):
        
        valid_lines = filter(self.is_point, self.d)
        
        for l in valid_lines:

            self.points.add_point(self.get_point(l))
            
    
    def is_point(self):
        
        pass
    
    def get_point(self):
        
        pass
    
    def print_found_points(self):
        
        
        for p in self.points.listofpoints:
            p.dump_point()
            
    def export_points_toTXT(self, filepathname):
        
        file = open(filepathname,'w')
        
        for p in self.points.listofpoints:
            
            file.write(p.get_string_of_points()+"\n")
            
        file.close()
