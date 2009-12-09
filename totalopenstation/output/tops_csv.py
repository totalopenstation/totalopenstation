#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_csv.py
# Copyright 2008-2009 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import csv
import StringIO


class OutputFormat:

    """
    Exports points data in CSV format.

    ``data`` should be an iterable (e.g. list) containing one iterable
    (e.g.  tuple) for each point. The default order is PID, x, x, z,
    TEXT.

    This is consistent with our current standard.
    """

    def __init__(self, data):
        self.data = data
        self.output = StringIO.StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_NONNUMERIC)

    def process(self):
        self.writer.writerow(('PID', 'x', 'y', 'z', 'TEXT'))
        self.writer.writerows(self.data)
        return self.output.getvalue()

if __name__ == "__main__":
    TotalOpenCSV(
        [(1, 2, 3, 4, 'qwerty'),
         ("2.3", 42, 45, 12, 'asdfg')])
