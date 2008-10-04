#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: zeiss_elta_r55.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from generic import *


class ModelConnector(Connector):
    def __init__(self, port):
        Connector.__init__(self, port=port, bytesize=7)

class ModelParser(Parser):
    
    def __init__(self, filename):
        Parser.__init__(self, filename, swapXY=True)
    
    def is_point(self,line):

        tokens = {
            'sequence' : line[0:7],
            'pid' : line[8:27],
            'text' : line[27:32],
            'X_str' : line[36],
            'x' : line[38:50],
            'Y_str' : line[51],
            'y' : line[53:66],
            'Z_str' : line[67],
            'z' : line[69:80]
            }
        
        try:
            int(tokens['sequence'])
            int(tokens['pid'])
            float(tokens['x'])
            float(tokens['y'])
            float(tokens['z'])
        
        except (ValueError, IndexError):
            
            is_point = False
        
        else:
            
            is_point = True
        
        return is_point
    
    def get_point(self,line):
        '''Gets a point from a line retrieving basic data.'''
        
        tokens = {
            'pid' : line[8:27].strip(),   # the result is more elegant than
            'text' : line[27:32].strip(), # the code (Heisenberg rocks!)
            'x' : line[38:50].strip(),
            'y' : line[53:66].strip(),
            'z' : line[69:80].strip()
            }
        
        point_id = int(tokens['pid'])
        text = str(tokens['text'])
        
        # note that for now we keep floats into strings to avoid approximation
        # problems, provided that for writing DXF a string is sufficient.
        # FIXME before introducing new output formats.
        # We could use string formatting operations to store data as floats
        # and convert them to strings with the needed precision on the fly.
        
        x = str(tokens['x'])
        y = str(tokens['y'])
        z = str(tokens['z'])
            
        if self.swapXY is True:
            p = Point(point_id, y, x, z, text)
        else:
            p = Point(point_id, x, y, z, text)
        
        return p

