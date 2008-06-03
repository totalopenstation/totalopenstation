#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: zeiss_elta_r55.py

from generic import Connector, Parser

class ZeissConn(Connector):
    pass

class ZeissEltaR55(Parser):
    '''This is a quite old model.'''
    
    def is_point(self,line):
        '''Example line:
   0007                   1         X       -0.472 Y         1.576 Z     0.004 
        '''
        tokens = line.split()
        try:
            int(tokens[0])
            int(tokens[1])
            float(tokens[3])
            float(tokens[5])
            float(tokens[7])
        except (ValueError, IndexError):
            is_point = False
        else:
            is_point = True
        
        return is_point

    def get_point(self,line):
        tokens = line.split()
        point_id = int(tokens[1])
        x = float(tokens[3])
        y = float(tokens[5])
        z = float(tokens[7])
        return (point_id, x, y, z)

if __name__ == "__main__":
    main = ZeissEltaR55(open('../sample_data/zeiss_elta_r55').readlines())

