#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: trimble.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009,2011 Stefano Costa <steko@iosa.it>
# Copyright 2009 Alessandro Bezzi <alessandro.bezzi@arc-team.com>
# Under the GNU GPL 3 License

from . import *


class ModelConnector(Connector):

    """Trimble Geodimeter 600"""

    def __init__(self, port):
        Connector.__init__(
            self,
            port=port,
            baudrate=9600,
            bytesize=8,
            stopbits=1,
            parity='N')
