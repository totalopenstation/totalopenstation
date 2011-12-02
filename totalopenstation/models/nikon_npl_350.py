#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: nikon_npl_350.py
# Copyright 2008,2011 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from . import *


class ModelConnector(Connector):

    def __init__(self, port):
        Connector.__init__(self, port=port, baudrate=1200, xonxoff=True)
