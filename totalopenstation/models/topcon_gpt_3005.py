#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: topcon gpt 3005.py
# Copyright 2021 Enzo Cocca <enzo.ccc@gmail.com>


# This file is part of Total Open Station.

# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.


from . import Connector


class ModelConnector(Connector):

    def __init__(self, port):
        Connector.__init__(self, port=port, baudrate=9600 , bytesize=8)
