#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: upref.py
# Copyright 2010 Stefano Costa <steko@iosa.it>
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
import os
import os.path

from ConfigParser import ConfigParser, NoSectionError


class UserPrefs(ConfigParser):
    '''Manage user preferences for GUI options and last used values.

    Proof-of-concept. Notes:

    * user preferences path is hardcoded here
    * returns a dictionary of user preferences
    * preferences will be set through a dictionary as well'''


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
        print('User preferences do not exist!')
        self.add_section('topsconfig')
        self.set('topsconfig', 'model','')
        self.set('topsconfig', 'port', '')
        print('Created new user preferences file')

    def write(self):
        ''' override ConfigParser.write() method '''

        ConfigParser.write(self, open(self.upref, 'w'))

    def getdict(self):
        ''' get config file values '''

        model = self.get('topsconfig', 'model')
        port = self.get('topsconfig', 'port')

        return {'model':model , 'port': port}

    def getvalue(self, value):
        ''' get specific config file value '''

        return self.get('topsconfig', value)

    def setvalues(self, values):
        ''' set specific config file value '''

        self.set('topsconfig', 'model', values['model'])
        self.set('topsconfig', 'port', values['port'])

        self.write()
