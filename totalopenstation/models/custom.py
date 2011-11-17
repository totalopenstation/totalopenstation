#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: custom.py
# Copyright 2008 Luca Bianconi <luxetluc@yahoo.it>
# Copyright 2008,2011 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from . import Connector


class CustomConnector(Connector):

    def __init__(self, port, **kwargs):
        Connector.__init__(self, port=port, **kwargs)
