#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_dxf.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>
# Copyright 2025 Enzo Cocca <enzo.ccc@gmail.com>

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

import io
import ezdxf
from ezdxf.enums import TextEntityAlignment

from . import Builder


class OutputFormat(Builder):
    """
    Exports points data in AutoCAD DXF format using ezdxf library.

    This implementation uses ezdxf for robust DXF file generation,
    supporting modern AutoCAD versions while maintaining compatibility.

    ``data`` should be an iterable (e.g. list) containing Feature objects.
    Each Feature has geometry (Point or LineString) and metadata (id, desc).
    """

    def __init__(self, data, separate_layers=True):
        self.data = data
        self.separate_layers = separate_layers
        self.text_height = 0.05

    def process(self):
        """Process the input data and return a string as output.

        This is because we want to keep the generation of output
        separated from saving it to disk.
        """
        # Create a new DXF document (R12 format for maximum compatibility)
        doc = ezdxf.new('R12')
        doc.header['$INSUNITS'] = 0  # Unitless
        msp = doc.modelspace()

        # Extract unique layer codes and assign colors
        codes = set([p.desc for p in self.data])
        codes = [c.replace('.', '_') for c in codes]
        colors = {code: (i % 255) + 1 for i, code in enumerate(codes)}

        # Create layers
        for code in codes:
            color = colors[code]
            if self.separate_layers:
                doc.layers.add(f"{code}_POINTS", color=color)
                doc.layers.add(f"{code}_Z_COORDS", color=color)
                doc.layers.add(f"{code}_LABELS", color=color)
            else:
                doc.layers.add(code, color=color)

        # Add entities
        for p in self.data:
            p_layer = p.desc.replace('.', '_')
            geom = p.geometry

            if geom.geom_type == 'Point':
                self._add_point_entity(msp, p, p_layer, geom)
            elif geom.geom_type == 'LineString':
                self._add_linestring_entity(msp, p, p_layer, geom)
            else:
                raise NotImplementedError(
                    f"Geometry type '{geom.geom_type}' is not supported"
                )

        # Export to string
        stream = io.StringIO()
        doc.write(stream)
        return stream.getvalue()

    def _add_point_entity(self, msp, feature, p_layer, geom):
        """Add a Point entity with associated text labels."""
        if self.separate_layers:
            layer_point = f"{p_layer}_POINTS"
            layer_z_text = f"{p_layer}_Z_COORDS"
            layer_id_text = f"{p_layer}_LABELS"
        else:
            layer_point = layer_z_text = layer_id_text = p_layer

        x, y = float(geom.x), float(geom.y)

        # Add point entity
        try:
            z = float(geom.z)
            msp.add_point((x, y, z), dxfattribs={'layer': layer_point})
        except (ValueError, AttributeError):
            z = None
            msp.add_point((x, y), dxfattribs={'layer': layer_point})

        # Add ID text
        msp.add_text(
            str(feature.id),
            dxfattribs={
                'layer': layer_id_text,
                'height': self.text_height,
            }
        ).set_placement((x, y), align=TextEntityAlignment.LEFT)

        # Add Z value text (below the point)
        if z is not None:
            y_offset = y - (self.text_height * 1.2)
            msp.add_text(
                str(z),
                dxfattribs={
                    'layer': layer_z_text,
                    'height': self.text_height,
                }
            ).set_placement((x, y_offset), align=TextEntityAlignment.LEFT)

    def _add_linestring_entity(self, msp, feature, p_layer, geom):
        """Add a LineString entity as a polyline."""
        layer = p_layer if not self.separate_layers else p_layer

        # Build list of vertices with 3D coordinates
        vertices = []
        for coord in geom.coords:
            if len(coord) >= 3:
                vertices.append((coord[0], coord[1], coord[2]))
            else:
                vertices.append((coord[0], coord[1], 0))

        # Add 3D polyline
        msp.add_polyline3d(
            vertices,
            dxfattribs={'layer': layer}
        )
