#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: prova.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from output.dxf.sdxf import *
from models.zeiss_elta_r55 import *

# read TS data

main = ZeissEltaR55(open('models/zeiss_elta_r55_20080717.raw').readlines())

codici = set([ p[4] for p in main.points ])

# create DXF

#Drawing
d=Drawing(layers=())
#tables
d.styles.append(Style())                #table styles
d.styles.append(Style( name='GQB', height=0.04 ))
d.views.append(View('Normal'))          #table view
d.views.append(ViewByWindow('Window',leftBottom=(1,0),rightTop=(2,1)))  #idem

for n, i in enumerate(codici):
    name_p = "%s_PUNTI" % i
    name_q = "%s_QUOTE" % i
    name_n = "%s_NUMERI" % i
    d.append(Layer(name=name_p, color=n))
    d.append(Layer(name=name_q, color=n))
    d.append(Layer(name=name_n, color=n))

for p in main.points:
    p_id, p_x, p_y, p_z, p_layer = p
    name_p = "%s_PUNTI" % p_layer
    name_q = "%s_QUOTE" % p_layer
    name_n = "%s_NUMERI" % p_layer
    
    # add point
    d.append(Point(points=[(p_x, p_y, 0)], layer=name_p, color=256))
    
    # add ID number
    d.append(Text(str(p_id),point=(p_x, p_y, 0), layer=name_n ))
    
    # add Z value
    d.append(Text(str(p_z), point=(p_x, p_y, 0), layer=name_q ))

d.saveas('gqb.dxf')

