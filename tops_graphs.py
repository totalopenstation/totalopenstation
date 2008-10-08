#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_graphs.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com> and Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from pylab import *

class Graph2D:
    
    def __init__(self, pnts = None):
        
        self.points = pnts
        
    def plot_data(self):
        
        pass


class Graph3D:
    
    def __init__(self, pnts = None):
        
        self.points = pnts
        
    def plot_data(self):
        
        pass


if __name__ == '__main__':
    
    Graph2D()
    
    Graph3D()