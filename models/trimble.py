#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: trimble.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from generic import *


class ModelConnector(Connector):
    def __init__(self, port):
        Connector.__init__(self, port=port, baudrate=19200)


class ModelParser(Parser):
    
    def is_point(self,line):
        
        is_point = False

        if "37=" in line and "38=" in line and "39=" in line:
            is_point = True
    
        return is_point

    def get_point(self,chunk):
        tokens = {}
        lines = chunk.splitlines()
        for i in lines:
            if i.startswith('37='):
                tokens['x'] = i.split('=')[1]
            if i.startswith('38='):
                tokens['y'] = i.split('=')[1]
            if i.startswith('39='):
                tokens['z'] = i.split('=')[1]
        tokens['text'] = lines[0]
        try:
            p = Point('', tokens['x'], tokens['y'], tokens['z'], '')
        except KeyError:
            pass
        else:
            return p

    def split_points(self):
        splitted_points = self.data.split('5=')
        return splitted_points

