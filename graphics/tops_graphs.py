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

from rpy import r

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
        self.rmap = raster_import_ryan(self.points)
        self.plot_data()



        
    def plot_data(self):
        
        self.rmap.draw_map(imin=0, imax=349, center=1, scale=1)
        #self.rmap.line_3d(imin=100, imax=150,              center=1, scale=1)

 
class GraphSimple:
    
    def __init__(self, pnts = None):
        
        self.points = []
        self.getPoints(pnts)
        
        #self.points = pnts
        self.plotPts()

        
    def getPoints(self, f):
        
        #file= open(f,"r").readlines()
        
        for l in f:#file:
            
            self.points.append(self.getXYPoint(l))
        
    def getXYPoint(self, line):
        
        l = line#.split(",")
        
        return [l[1],l[2]]
    
    def getXYZPoint(self, line):
        
        l = line#.split(",")
        
        return [l[1],l[2],l[3]]
        
    def plotPts(self):
        
        if len(self.points[0]) < 3:
            
            x = [float(x[0]) for x in self.points]
            y = [float(y[1]) for y in self.points]
            
            r.png('output.png')
    
            r.plot(x,y, xlab='x', ylab='y', main='TOPS-preview graph')
            
        else:
            
            x = [float(x[0]) for x in self.points]
            y = [float(y[1]) for y in self.points]
            z = [float(z[1]) for z in self.points]
            
            r.png('output.png')
    
            r.plot(x,y, xlab='x', ylab='y', main='TOPS-preview graph')
            r.lines(x, z, col='red')


class GraphPersonal:
    
    def __init__(self, pnts = None):
        
        self.points = open(pnts).readlines()
        self.plot_data()
        
    def plot_data(self):
        i=0
        for p in self.points:
            
            ps = p.split(",")
            if len(ps) == 3:
                x = ps[0]
                x = float(x)
                x= (x-450000)/1000
                
                y = ps[1]
                y = float(y)
                y = (y-205000)/1000
                
                z = ps[2]
                z = float(z)
                z = (z-62000)/1000
                
                box(pos = (x+i, y+i, z+i), size = (x,y,z), color = color.green)
                i = i+1


#class Mat3DMap:
    
    #def __init__(self, pnts = None):

        #A = array(pnts) 
        #M.plot3_points(A,precision=1)



if __name__ == '__main__':
    
    #Graph2D()
    
    #Graph3D([(10,10,10),(5,5,5)])
    
    #GraphRasterMap("../leicatest.txt")
    #GraphRasterMap("test.txt")
    
    #Mat3DMap([(10,10,10),(5,5,5)])
    
    #GraphSimple("../leicatest.txt")
    
    GraphPersonal("../leicatest.txt")
