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
        
        self.open()
    
    def download(self):
        '''Download method for user interfaces.
        
        Firts the class must be instantiated, then the port is open and the
        transfer from the device can start. Once the transfer is finished
        the user interface should call this method.'''
        
        n = self.inWaiting()
        result = self.read(n)
    
        # looks like there is a maximum buffer of 4096 characters, so we have
        # to wait for a short time and iterate the process until finished
        
        sleep(0.1)
        
        while self.inWaiting() > 0:
            result = result + self.read(self.inWaiting())
            sleep(0.1)
        
        self.result = result
        return self.result

class Point:
    
    def __init__(self, p_id, x, y, z, text):
        
        self.p_id= p_id
        self.x=x
        self.y=y
        self.z=z
        self.text=text
        
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
        
    def list_to_tuple(self):
        
        list_aux=[]
        for p in self.listofpoints:
            list_aux.append(p.point_to_tuple())
        return list_aux

class Data:
    
    def __init__(self):
        pass
        
    def data_from_txt_file(self, filepathname):
        
        file = open(filepathname,'r')
        self.lines = file.readlines()
        file.close()


class TotalStation:
    
    def __init__(self,filename,swapXY=False):
        
        #self.d = Data()
        #self.d.data_from_txt_file(filename)
        self.d = open(filename).readlines()
        self.points = PointsList()
        self.swapXY = swapXY
        
        self.parse_retrieve_data()
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
