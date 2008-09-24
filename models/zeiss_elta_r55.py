#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: zeiss_elta_r55.py

from generic import *

class ZeissConn(Connector):
    pass

class ZeissEltaR55(TotalStation):
    
    def __init__(self, filename):
        TotalStation.__init__(self, filename, swapXY=True)
    
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
        
        text = line[27:32].split()
        
        if len(text) >= 1 :
            aux = text[0]
        else:
            aux = ""
        
        tokens = {
            'pid' : line[8:27].split()[0],   # the result is more elegant than
            'text' : aux,                    # the code (Heisenberg rocks!)
            'x' : line[38:50].split()[0],
            'y' : line[53:66].split()[0],
            'z' : line[69:80].split()[0]
            }
                    
        point_id = int(tokens['pid'])
        text = str(tokens['text'])
        
        # note that for now we keep floats into strings to avoid approximation
        # problems, provided that for writing DXF a string is sufficient.
        # FIXME before introducing new output formats.
        
        x = str(tokens['x'])
        y = str(tokens['y'])
        z = str(tokens['z'])
            
        if self.swapXY is True:
            p = Point(point_id, y, x, z, text)
        else:
            p = Point(point_id, x, y, z, text)
        
        return p

