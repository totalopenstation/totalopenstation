#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-
# filename: total.py

from __future__ import with_statement


class TotalStation:
    """Reads input data from a text file.
    
    The input file is the output from the total station, with data on each
    line. The first lines contain general information, points from 0007 on
    contain the XYZ coordinates of points, one per line.
    """
    
    def get_points(self,data):
        """Gets points coordinates from the valid data lines."""
        
        for line in data:
            try:
                int(line[0]) and int(line[1]) and line[2] == 'X' and float(line[3])
            except ValueError:
                pass
            else:
                print "Point %d" % int(line[1])
                print line[2], "=", line[3].rjust(10)
                print line[4], "=", line[5].rjust(10)
                print line[6], "=", line[7].rjust(10)
                print "-------"
    
    def __init__(self,data):
        self.data = data
        with open(self.data, 'r') as data_file:
            valid_lines = [ elem for elem in data_file if elem != 'E\n' ]
        self.valid_data = [ line.split() for line in valid_lines ]
        self.get_points(self.valid_data)

if __name__ == "__main__":
    main = TotalStation('prova2')

