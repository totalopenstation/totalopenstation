#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_graphs.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com> and Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

#from pylab import *
from numpy import *
import pylab as p
import matplotlib.axes3d as p3

from raster_map import *

#import mat3d as M



class Graph2D:
    
    def __init__(self, pnts = None):
        
        self.points = pnts
        
    def plot_data(self):
        
        pass



class Graph3D:

    def __init__(self, pnts = None):
        
        self.points = pnts
        self.create_grid()
        self.set_data()
        self.plot_data()
    
    def create_grid(self):
        
        self.X,self.Y = meshgrid((0,20,1),(0,20,1))
        
        self.Z = zeros((len(self.X),len(self.Y)),'Float32')
        
    def set_data(self):
        
        for p in self.points:
            x,y,z = p
            ix = int(x / 10)
            iy = int(y / 10)
            self.Z[iy, ix] = z

        
    def plot_data(self):
        
        fig = p.figure()
        ax = p3.Axes3D(fig)
        ax.plot_wireframe(self.X, self.Y, self.Z)
        p.show()

class GraphRasterMap:
    
    def __init__(self, pnts = None):
        
        self.points = pnts
        topog = raster_import_ryan(self.points)
        topog.draw_map()



        
    def plot_data(self):
        
        pass

#class Mat3DMap:
    
    #def __init__(self, pnts = None):

        #A = array(pnts) 
        #M.plot3_points(A,precision=1)

if __name__ == '__main__':
    
    #Graph2D()
    
    #Graph3D([(10,10,10),(5,5,5)])
    
    #GraphRasterMap("../leicatest.txt")
    GraphRasterMap("test.txt")
    
    #Mat3DMap([(10,10,10),(5,5,5)])