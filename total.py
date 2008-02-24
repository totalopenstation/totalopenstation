#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

from __future__ import with_statement


class TotalStation ():
    """Reads input data from a text file."""
    
    def get_points(self,data):
        for line in data:
            try:
                int(line[0]) and int(line[1])
            except ValueError:
                pass
            else:
                print "Point %d" % int(line[1])
                print "%s = %s" % (line[2], line[3])
                print "%s = %s" % (line[4], line[5])
                print "%s = %s" % (line[6], line[7])
                print "-------"
    
    def __init__(self,data):
        self.data = data
        with open(self.data, 'r') as data_file:
            valid_lines = [ elem for elem in data_file if elem != 'E\n' ]
        self.valid_data = [ line.split() for line in valid_lines ]
        self.get_points(self.valid_data)

if __name__ == "__main__":
    main = TotalStation('prova2')

