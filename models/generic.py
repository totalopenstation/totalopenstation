#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: generic.py

import serial

class Connector:
    pass

class Parser:
    """Reads input data retrieved from a total station.
    
    More detailed description needed here.
    """
    
    def __init__(self,data,swapXY=False):
        self.data = data
        self.swapXY = swapXY
        valid_lines = filter(self.is_point, data)
        valid_points = map(self.get_point, valid_lines)
        #print valid_points
        self.points = valid_points
        
    def is_point(self):
        pass
    def get_point(self):
        pass
    def is_origin(self):
        pass
    def get_origin(self):
        pass

