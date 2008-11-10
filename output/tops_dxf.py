#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_dxf.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


class TotalOpenDXF:
    
    """
    Exports points data in AutoCAD DXF format.
    
    It is based on the official DXF2000 documentation. Works with AutoCAD 2005.
    
    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.
    
    This is consistent with our current standard.
    """
    
    def __init__(self,data,filepath,separate_layers=True):
        
        self.data = data
        self.dxf_file = filepath
        self.separate_layers = separate_layers
        self.result = '  0\nSECTION\n  2\nENTITIES\n'
        self.text_height = 0.05
        
        self.codes = set([ p[4] for p in self.data ])
        
        self.layers = dict(enumerate(self.codes))
        self.colors = dict(zip(self.layers.values(), self.layers.keys()))
        
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
            self.result = '%s  0\nPOINT\n  8\n%s\n  10\n%s\n  20\n%s\n  62\n%s\n' % (self.result, layer_point, p_x, p_y, self.colors[p_layer])
            
            # add ID number
            self.result = '%s  0\nTEXT\n  8\n%s\n  10\n%s\n  20\n%s\n  62\n%s\n  40\n%01.2f\n  1\n%s\n' % (self.result, layer_id_text, p_x, p_y, self.colors[p_layer], self.text_height, p_id)
            
            # add Z value
            # d.append(Text(str(p_z), point=(p_x, p_y, 0), layer=name_q ))
            self.result = '%s  0\nTEXT\n  8\n%s\n  10\n%s\n  20\n%s\n  62\n%s\n  40\n%01.2f\n  1\n%s\n' % (self.result, layer_z_text, p_x, p_yz, self.colors[p_layer], self.text_height, p_z)
        
        self.result = self.result + '  0\nENDSEC\n  0\nEOF\n'
        self.output = open(self.dxf_file, 'w')
        self.output.write(self.result)
        self.output.close()


if __name__ == "__main__":
    TotalOpenDXF(
        [
            (1,2,3,4,'qwerty'),
            ("2.3",42,45,12,'asdfg')
        ],
    'p.dxf')

