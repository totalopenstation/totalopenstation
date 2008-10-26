#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_sql.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


def to_sql(point,tablename):
    '''Generate SQL line corresponding to the input point.
    
    At this moment the column names are fixed, but they could change in the
    future. The default names are reasonable.'''
    
    params = { 'wkt' : to_wkt(point),
        'tablename' : tablename,
        'pid' : point[0],
        'text' : point[4]}
    sql_string = "INSERT INTO %(tablename)s (point_id, point_geom, point_text) VALUES (%(pid)s,GeomFromText('%(wkt)s'),'%(text)s');\n" % params
    return sql_string

def to_wkt(point):
    pid, x, y, z, text = point
    wkt_representation = 'POINT(%s %s)' % (x, y)
    return wkt_representation

class TotalOpenSQL:
    
    """
    Exports points data in SQL format suitable for use with PostGIS & friends.
    
    http://postgis.refractions.net/documentation/manual-1.3/ch04.html#id2986280
    has an example of loading an SQL file into a PostgreSQL database.
    
    ``data`` should be an iterable (e.g. list) containing one iterable (e.g.
    tuple) for each point. The default order is PID, x, x, z, TEXT.
    
    This is consistent with our current standard.
    """
    
    def __init__(self,data,filepath,tablename):
        output = open(filepath, "wb")
        lines = [ to_sql(e,tablename) for e in data ]
        lines.insert(0,'BEGIN;\n')
        lines.append('COMMIT;\n')
        output.writelines(lines)
        output.close()


if __name__ == "__main__":
    TotalOpenSQL(
        [
            (1,2,3,4,'qwerty'),
            ("2.3",42,45,12,'asdfg')
        ],
    'tops.sql','prova')

