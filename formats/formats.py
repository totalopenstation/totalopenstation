#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: totalopenstation-cli-parser.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>
# Copyright 2008-2009 Luca Bianconi <luxetluc@yahoo.it>

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

formats = {
    'Leica TCR 1205' : 'leica_tcr_1205',
    'Zeiss REC 500' : 'zeiss_rec_500',
    'Nikon Npl 350' : 'nikon_npl_350',
    'Leica TCR 705' : 'leica_tcr_705',
    'Trimble AREA' : 'trimble_are',
    }

def list_formats():
    mod_string = "List of supported input formats:\n" + "-"*20+ "\n"
    for k,v in sorted(formats.items()):
        mod_string += k.ljust(20) + v + "\n"
    mod_string += "\n"
    return mod_string

if __name__ == '__main__':
    print list_formats()
