#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com>
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


class OutputFormat:

    """
    Exports points data in TXT format line by line.

    ``data`` should be an iterable (e.g. list) containing one iterable
    (e.g.  tuple) for each point. The default order is PID, x, y, z,
    TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data, filepath):

        file = open(filepath, 'w')
        for d in data:
            string = "%s %s %s\n" % (d[1], d[2], d[3])
            file.write((str(string)))
        file.close()

if __name__ == "__main__":
    TotalOpenTXT(
        [(1, 2, 3, 4, 'qwerty'),
         ("2.3", 42, 45, 12, 'asdfg')],
    'p.txt')
