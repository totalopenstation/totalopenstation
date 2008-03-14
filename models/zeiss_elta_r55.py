#! /usr/bin/env python2.5
# -*- coding: utf-8 -*-

def is_origin(line):
    tokens = line.split()
    try:
        int(tokens[0])
    except ValueError:
        n = False
    else:
        n = True
    
    
    
    return n and tokens[1] == '0S'

def get_origin(line):
    tokens = line.split()
    x = float(tokens[3])
    y = float(tokens[5])
    z = float(tokens[7])
    return x, y, z

