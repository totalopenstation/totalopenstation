#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: upref.py
# Copyright 2010,2013 Stefano Costa <steko@iosa.it>
# Copyright 2010 Luca Bianconi <luxetluc@yahoo.it>
#
# This file is part of Total Open Station.
#
# Total Open Station is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Total Open Station is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Total Open Station.  If not, see
# <http://www.gnu.org/licenses/>.

import atexit
import logging
import os
import os.path

from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class UserPrefs(ConfigParser):
    '''Manage user preferences for GUI options and last used values.

    Proof-of-concept. Notes:

    * user preferences path is hardcoded here
    * returns a dictionary of user preferences
    * preferences will be set through a dictionary as well'''

    OPTIONS = {
        'model': '',
        'port': '',
        'sleeptime': 1.0,       # added in 0.3.1
    }

    def __init__(self):

        ConfigParser.__init__(self)

        USER_PREFS_PATH = '~/.totalopenstation/totalopenstation.cfg'

        self.upref = os.path.expanduser(USER_PREFS_PATH)

        if os.path.exists(self.upref):
            self.read(self.upref)
            try:
                self.getvalue('model')
            except NoSectionError:
                self.initfile()
        elif not os.path.exists(os.path.dirname(self.upref)):
            os.mkdir(os.path.dirname(self.upref))
            self.initfile()
        else:
            self.initfile()

    def initfile(self):
        self.write()
        logging.info('User preferences do not exist!')
        self.add_section('topsconfig')
        for k,v in self.OPTIONS.items():
            self.set('topsconfig', k, v)
        logging.info('Created new user preferences file with default values')

    def write(self):
        ''' override ConfigParser.write() method '''

        ConfigParser.write(self, open(self.upref, 'w'))

    def getdict(self):
        ''' get config file values '''

        current_options = {}
        for k in self.OPTIONS.keys():
            current_options[k] = self.getvalue(k)

        return current_options

    def getvalue(self, key):
        ''' get specific config file value '''

        try:
            value = self.get('topsconfig', key)
        except NoOptionError:
            value = self.OPTIONS[key] # use default value
        return value

    def setvalues(self, values):
        ''' set specific config file value '''

        for k, v in values.items():
            self.set('topsconfig', k, v)

        self.write()
