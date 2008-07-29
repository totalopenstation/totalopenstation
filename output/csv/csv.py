#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: csv.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

import csv

writer = csv.writer(open("some.csv", "wb"))
writer.writerows(someiterable)

