#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: zeiss_elta_r55.py

from generic import Connector, Parser

class ZeissConn(Connector):
    pass

class ZeissEltaR55(Parser):
    '''This is a quite old model.'''
    
    def __init__(self, data):
        Parser.__init__(self, data, swapXY=True)
    
    def is_point(self,line):
        '''Example line:
   0007                   1         X       -0.472 Y         1.576 Z     0.004 
        '''
        
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
        tokens = {
            'pid' : line[8:27],
            'text' : line[27:32],
            'x' : line[38:50],
            'y' : line[53:66],
            'z' : line[69:80]
            }
        
        point_id = int(tokens['pid'])
        
        # note that for now we keep floats into strings to avoid approximation
        # problems, provided that for writing DXF a string is sufficient.
        # FIXME before introducing new output formats.
        
        x = str(tokens['x'])
        y = str(tokens['y'])
        z = str(tokens['z'])
        text = str(tokens['text'])
        
        if self.swapXY is True:
            return (point_id, y, x, z, text)
        else:
            return (point_id, x, y, z, text)

if __name__ == "__main__":
    main = ZeissEltaR55(open('zeiss_elta_r55_20080704.raw').readlines())

