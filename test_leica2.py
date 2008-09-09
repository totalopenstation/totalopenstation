#! /usr/bin/env python
# -*- coding: utf-8 -*-
# filename: prova_leica.py
# Copyright 2008 Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License

from output.dxf.sdxf import *
from models import leica_tcr_1205
from dxfexporter import *

# read TS data

main = leica_tcr_1205.LeicaTCR1205('models/leica_1205_1.txt')
dxf = DXFexporter(main.t_points)
dxf.export_Dxf_ToFile(dxf.dxf_doc,'leica.dxf')
