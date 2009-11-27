#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_dat.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import StringIO

def to_dat(e):
    if e[4].endswith("R"):
        string = "%s %s %s %s\r\n" % (e[0], e[0], e[1], e[2])
        return string
    else:
        return ''


class TotalOpenDAT:
    
    """
    Exports points data in DAT format suitable for use with Archis.
    
    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.
    
    This is consistent with our current standard.
    """
    
    def __init__(self,data):
        self.data = data

    def process(self):
        output = StringIO.StringIO()
        lines = [ to_dat(e) for e in self.data ]
        output.writelines(lines)
        return output.getvalue()


if __name__ == "__main__":
    TotalOpenDAT(
        [
            (1,2,3,4,'qwerty'),
            ("2.3",42,45,12,'asdfg')
            ]
        )

