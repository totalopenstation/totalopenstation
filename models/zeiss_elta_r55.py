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
        tokens = line.split()
        try:
            int(tokens[0])
            int(tokens[1])
            #float(tokens[3])
            #float(tokens[5])
            #float(tokens[7])
        except (ValueError, IndexError):
            is_point = False
        else:
            is_point = True
        
        return is_point

    def get_point(self,line):
        tokens = line.split()
        point_id = int(tokens[1])
        if tokens[2] == 'X':
            x = str(tokens[3])
            y = str(tokens[5])
            z = str(tokens[7])
            text = ""
        elif tokens[3] == 'X':
            x = str(tokens[4])
            y = str(tokens[6])
            z = str(tokens[8])
            text = str(tokens[2])
        if self.swapXY is True:
            return (point_id, y, x, z, text)
        else:
            return (point_id, x, y, z, text)

if __name__ == "__main__":
    main = ZeissEltaR55(open('zeiss_elta_r55_20080704.raw').readlines())

