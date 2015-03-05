#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_dxf.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>

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


class OutputFormat:

    """
    Exports points data in AutoCAD DXF format.

    It is based on the official DXF2000 documentation. Works with AutoCAD
    versions ranging at least from 2005 up to 2009, and QCAD.

    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data, separate_layers=True):

        self.data = data
        self.separate_layers = separate_layers
        self.text_height = 0.05

    def process(self):
        '''Process the input data and return a string as output.

        This is because we want to keep separated the generation of output
        from saving it to disk.'''

        result = ''

        # header
        result += '999\nDXF created from Total Open Station\n'
        result += '  0\nSECTION\n'
        result += '  2\nHEADER\n'
        result += '  9\n$ACADVER\n'
        result += '  1\nAC1009\n' # R11

        # extract layer list
        codes = set([p[4] for p in self.data])
        codes = [c.replace('.','_') for c in codes]
        layers = dict(enumerate(codes))
        colors = dict(zip(layers.values(), layers.keys()))

        # layer table
        result += '  0\nSECTION\n  2\nTABLES\n  0\nTABLE\n  2\nLAYER\n'
        for l in codes:
            if self.separate_layers is True:
                result += '  0\nLAYER\n'           # start definition of LAYER
                result += '  5\n10\n'              # LAYER handle
                result += '  2\n%s_PUNTI\n' % l    # LAYER name
                result += ' 70\n0\n'              # LAYER is not frozen
                result += ' 62\n%s\n' % (int(colors[l]) + 1) # LAYER color
                result += '  6\nCONTINUOUS\n'      # LAYER linetype

                result += '  0\nLAYER\n'           # same as above
                result += '  5\n10\n'
                result += '  2\n%s_QUOTE\n' % l
                result += ' 70\n0\n'
                result += ' 62\n%s\n' % (int(colors[l]) + 1)
                result += '  6\nCONTINUOUS\n'

                result += '  0\nLAYER\n'           # ditto
                result += '  5\n10\n'
                result += '  2\n%s_NUMERI\n' % l
                result += ' 70\n0\n'
                result += ' 62\n%s\n' % (int(colors[l]) + 1)
                result += '  6\nCONTINUOUS\n'
            else:
                result += '  0\nLAYER\n'           # ditto
                result += '  5\n10\n'
                result += '  2\n%s\n' % l          # LAYER name w/o any suffix
                result += ' 70\n0\n'
                result += ' 62\n%s\n' % (int(colors[l]) + 1)
                result += '  6\nCONTINUOUS\n'

        result += '  0\nENDTAB\n  0\nENDSEC\n'

        # drawing entities
        result += '  0\nSECTION\n  2\nENTITIES\n'

        for p in self.data:
            p_id, p_x, p_y, p_z, p_layer = p
            if self.separate_layers is True:
                layer_point = "%s_PUNTI" % p_layer
                layer_z_text = "%s_QUOTE" % p_layer
                layer_id_text = "%s_NUMERI" % p_layer
            else:
                layer_point = layer_z_text = layer_id_text = p_layer
            p_yz = str(float(p_y) - (self.text_height * 1.2))

            # add point
            result += '  0\nPOINT\n'
            result += '  8\n%s\n' % layer_point
            result += ' 10\n%s\n' % p_x
            result += ' 20\n%s\n' % p_y

            # add ID number
            result += '  0\nTEXT\n'
            result += '  1\n%s\n' % p_id
            result += '  8\n%s\n' % layer_id_text
            result += ' 10\n%s\n' % p_x
            result += ' 20\n%s\n' % p_y
            result += ' 40\n%01.2f\n' % self.text_height
            result += ' 62\n256\n'

            # add Z value as string
            result += '  0\nTEXT\n'
            result += '  1\n%s\n' % p_z
            result += '  8\n%s\n' % layer_z_text
            result += ' 10\n%s\n' % p_x
            result += ' 20\n%s\n' % p_yz
            result += ' 40\n%01.2f\n' % self.text_height
            result += ' 62\n256\n'

        result += '  0\nENDSEC\n  0\nEOF\n'
        return result
