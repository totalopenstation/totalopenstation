#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_interface.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com> and Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License



from optparse import OptionParser

class ParamSet:
    
    def __init__(self, progname):
        
        usage = "usage: "+progname+" [option] arg1 [option] arg2 ..."

        
        self.parser = OptionParser(usage = usage)
        
        self.parser.add_option("-i", "--inputfile",action="store", type="string",dest="infile",help="read input FILE", metavar="FILE")

        self.parser.add_option("-o", "--outputfile", action="store", type="string",dest="outfile",help="write output FILE", metavar="FILE")

        self.parser.add_option("-t", "--totalstation",action="store", type="string", dest="tsmodel",help="chose total station model STRING",metavar="STRING")

        self.parser.add_option("-e", "--exportformat",action="store", type="string", dest="exformat",help="chose export format typing the exstension's three chars STRING", metavar="STRING")

        (self.options, self.args) = self.parser.parse_args()
        
        if (self.options.infile == None)or(self.options.outfile == None)or(self.options.tsmodel == None)or(self.options.exformat == None):
            self.parser.error( """ Insert all the four arguments, please! """ )





if __name__ == '__main__':
    
    params = ParamSet("Tops")
    
    print params.options.infile