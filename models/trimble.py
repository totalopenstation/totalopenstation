#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: trimble.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009 Stefano Costa <steko@iosa.it>
# Copyright 2009 Alessandro Bezzi <alessandro.bezzi@arc-team.com>
# Under the GNU GPL 3 License

from generic import *


class ModelConnector(Connector):

    """Trimble Geodimeter 600"""

    def __init__(self, port):
        Connector.__init__(
            self,
            port=port,
            baudrate=9600,
            bytesize=8,
            stopbits=1,
            parity='N'
            )


class ModelParser(Parser,swapXY=True):

    def is_point(self,line):

        is_point = False

        if "5=" and "4=" and "37=" and "38=" and "39=" in line:
            is_point = True

        return is_point

    def get_point(self,chunk):
        tokens = {}
        lines = chunk.splitlines()
        for i in lines:
            if i.startswith('5='):
                tokens['n'] = i.split('=')[1]
            if i.startswith('4='):
                tokens['p'] = i.split('=')[1]
            if i.startswith('37='):
                tokens['x'] = i.split('=')[1]
            if i.startswith('38='):
                tokens['y'] = i.split('=')[1]
            if i.startswith('39='):
                tokens['z'] = i.split('=')[1]
        tokens['text'] = lines[0]

        try:
            p = Point(
                tokens['n'],
                tokens['x'],
                tokens['y'],
                tokens['z'],
                tokens['p']
                )
        except KeyError:
            pass
        else:
            return p

    def split_points(self):
        splitted_points = self.data.split('0=')
        return splitted_points

