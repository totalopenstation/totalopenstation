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


from . import Builder


class OutputFormat(Builder):

    """
    Exports points data in AutoCAD DXF format.

    It is based on the official DXF2000 documentation. Works with AutoCAD
    versions ranging at least from 2005 up to 2009, and QCAD.

    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, y, z, TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data, separate_layers=True):

        self.data = data
        self.separate_layers = separate_layers
        self.text_height = 0.05

    def process(self):
        '''Process the input data and return a string as output.

        This is because we want to keep the generation of output
        separated from saving it to disk.'''

        result = ''

        # header
        result += '999\nDXF created from Total Open Station\n'
        result += '  0\nSECTION\n'
        result += '  2\nHEADER\n'
        result += '  9\n$ACADVER\n'
        result += '  1\nAC1009\n' # R11
        result += '  0\nENDSEC\n'

        # extract layer list
        codes = set([p.desc for p in self.data])
        codes = [c.replace('.','_') for c in codes]
        layers = dict(enumerate(codes))
        colors = dict((i, j % 255) for i, j in zip(list(layers.values()), list(layers.keys())))

        # layer table
        result += '  0\nSECTION\n  2\nTABLES\n  0\nTABLE\n  2\nLAYER\n'
        for l in codes:
            if self.separate_layers is True:
                result += '  0\nLAYER\n'           # start definition of LAYER
                result += '  5\n10\n'              # LAYER handle
                result += f'  2\n{l}_POINTS\n'    # LAYER name
                result += ' 70\n0\n'              # LAYER is not frozen
                result += f' 62\n{int(colors[l]) + 1}\n' # LAYER color
                result += '  6\nCONTINUOUS\n'      # LAYER linetype

                result += '  0\nLAYER\n'           # same as above
                result += '  5\n10\n'
                result +=  f'  2\n{l}_Z_COORDS\n'
                result += ' 70\n0\n'
                result += f' 62\n{int(colors[l]) + 1}\n'
                result += '  6\nCONTINUOUS\n'

                result += '  0\nLAYER\n'           # ditto
                result += '  5\n10\n'
                result += f'  2\n{l}_LABELS\n'
                result += ' 70\n0\n'
                result += f' 62\n{int(colors[l]) + 1}\n'
                result += '  6\nCONTINUOUS\n'
            else:
                result += '  0\nLAYER\n'           # ditto
                result += '  5\n10\n'
                result += f'  2\n{l}\n'          # LAYER name w/o any suffix
                result += ' 70\n0\n'
                result += f' 62\n{int(colors[l]) + 1}\n'
                result += '  6\nCONTINUOUS\n'

        result += '  0\nENDTAB\n  0\nENDSEC\n'

        # drawing entities
        result += '  0\nSECTION\n  2\nENTITIES\n'

        for p in self.data:
            p_layer = p.desc
            geom = p.geometry
            if geom.geom_type == 'Point':
                if self.separate_layers is True:
                    layer_point = f"{p_layer}_POINTS"
                    layer_z_text = f"{p_layer}_Z_COORD"
                    layer_id_text = f"{p_layer}_LABELS"
                else:
                    layer_point = layer_z_text = layer_id_text = p_layer
                p_yz = str(float(geom.y) - (self.text_height * 1.2))

                # add point
                result += '  0\nPOINT\n'
                result += f'  8\n{layer_point}\n'
                result += f' 10\n{geom.x}\n'
                result += f' 20\n{geom.y}\n'

                # add ID number
                result += '  0\nTEXT\n'
                result +=  f'  1\n{p.id}\n'
                result +=  f'  8\n{layer_id_text}\n'
                result +=  f' 10\n{geom.x}\n'
                result +=  f' 20\n{geom.y}\n'
                result += f' 40\n{self.text_height:01.2f}\n' 
                result += ' 62\n256\n'

                try:
                    geom.z
                except ValueError:
                    pass
                else:
                    # add Z value as string
                    result += '  0\nTEXT\n'
                    result +=  f'  1\n{geom.z}\n'
                    result +=  f'  8\n{layer_z_text}\n'
                    result +=  f' 10\n{geom.x}\n'
                    result +=  f' 20\n{p_yz}\n'
                    result += f' 40\n{self.text_height:01.2f}\n'
                    result += ' 62\n256\n'

            elif geom.geom_type == 'LineString':
                result += '  0\nPOLYLINE\n'
                result +=  f'  8\n{p_layer}\n'
                result += '  6\nCONTINUOUS\n'
                result += ' 62\n256\n'
                result += ' 66\n1\n'
                result += ' 70\n0\n'
                for v in geom.coords:
                    result += '  0\nVERTEX\n'
                    result +=  f'  8\n{p_layer}\n'
                    result +=  f' 10\n{v[0]}\n' # x
                    result +=  f' 20\n{v[1]}\n' # y
                    try:
                        result +=  f' 30\n{v[2]}\n' # z
                    except IndexError:
                        result += ' 30\n0\n'
                result += '  0\nSEQEND\n'
            else:
                raise NotImplementedError
        result += '  0\nENDSEC\n  0\nEOF\n'
        return result
