#!/usr/bin/env python
#-*- coding:utf-8 -*-

import atexit
import os
import os.path

from ConfigParser import ConfigParser


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
            print('User preferences exist')
            self.read(self.upref)


        else:
            os.mkdir(os.path.dirname(self.upref))
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
