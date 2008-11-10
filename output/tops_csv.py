#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import csv

class TotalOpenCSV:
    
    """
    Exports points data in CSV format.
    
    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.
    
    This is consistent with our current standard.
    """
    
    def __init__(self,data,filepath):
        writer = csv.writer(open(filepath, "wb"), quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(('PID', 'x', 'y', 'z', 'TEXT'))
        writer.writerows(data)

if __name__ == "__main__":
    TotalOpenCSV(
        [
            (1,2,3,4,'qwerty'),
            ("2.3",42,45,12,'asdfg')
        ],
    'p.csv')

