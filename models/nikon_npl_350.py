#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: nikon_npl_350.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from generic import *


class ModelConnector(Connector):
    def __init__(self, port):
        Connector.__init__(self, port=port)

class ModelParser(Parser):
    
    def __init__(self, data):
        Parser.__init__(self, data)
    
    def is_point(self,line):
        return True
    
    def get_point(self,line):
        '''Gets a point from a line retrieving basic data.'''
        
        try:
            sp_line = line.split(",")
            tokens = {
                'code' : sp_line[0],
                'pid' : sp_line[1],
                'text' : sp_line[7],
                'x' : sp_line[4],
                'y' : sp_line[3],
                'z' : sp_line[5]
                }
            
            assert tokens['code'] == 'SS'
            int(tokens['pid'])
            float(tokens['x'])
            float(tokens['y'])
            float(tokens['z'])
        
        except (AssertionError, ValueError, IndexError):
            pass
        
        else:
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

            p = Point(point_id, y, x, z, text)

            return p

