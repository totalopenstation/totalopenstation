#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: zeiss_elta_r55.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from generic import *


class ModelConnector(Connector):

    def __init__(self, port):
        Connector.__init__(self, port=port, bytesize=7)
