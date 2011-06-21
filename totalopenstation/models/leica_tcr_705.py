#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: leica_tcr_705.py
# Copyright 2009 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2009,2011 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from . import *


class ModelConnector(Connector):

    def __init__(self, port):
        Connector.__init__(self, port=port, baudrate=19200)
