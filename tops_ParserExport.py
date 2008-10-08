#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_interface.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com> and Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


import sys
import os.path

from models import models
from tops_graphs import *
from tops_paramset import *


class Tops_ParserExport:

	def __init__(self):
		
		#to be entered maybe from a txt file containing the list of the supported models
		supportedTs = models.models.values()
		
		supportedExportFormats=("CSV","DXF","DAT","TXT")
		
                argsreader = ParamSet("Tops")
		
                fileToOpen = argsreader.options.infile
                tsModel = argsreader.options.tsmodel
                exportFormat = argsreader.options.exformat
                fileToSave = argsreader.options.outfile
                
                #argsreader.destroy()
		
		#if the entered string for chosing the export format is converted to an only upper case version

		if exportFormat.isupper() != True:
			exportFormat = exportFormat.upper()
		
		#check if the chosen forma is supported, else it dumps the supported ones
		if self.isInExportFormats(exportFormat, supportedExportFormats) != True:
			
			print "Incorrect Exporting format"
			print "Supported formats are: "
			for f in supportedExportFormats:
				print f
			
			sys.exit()
		
		if os.path.exists(fileToOpen) != True:
			
			sys.exit("Input Data File not existent"+"\n"+"Please chose a correct file name")
		
		if tsModel in supportedTs:
                    
                    self.goTS(tsModel,fileToOpen,exportFormat,fileToSave)
                    	
		else:
			print "Incorrect Total Station Model type!"
			print "Supported models are: "
			for ts in supportedTs:
				print ts
	                sys.exit()
	
	#check if the exporting format is correct
	def isInExportFormats(self,a, supF):
		
		found = False
		for f in supF:
			if f == a:
				found = True
				break
		
		return found
	
	#select the export type among the supported ones
	def exportAction(self,frmt,pnts,outName):
		
		if frmt == "CSV":
			
			from output.csv.tops_csv import TotalOpenCSV
			
			csv_output = TotalOpenCSV(pnts, (outName+'.csv'))
	
		elif frmt == "DXF":
			
			from output.dxf.tops_dxf import TotalOpenDXF
			
			dxf_output = TotalOpenDXF(pnts, (outName+'.dxf'))
			
		elif frmt == "DAT":
			
			from output.dat.tops_dat import TotalOpenDAT
			
			dat_output = TotalOpenDAT(pnts, (outName+'.dat'))
			
		elif frmt == "TXT":
		
			from output.txt.tops_txt import TotalOpenTXT
			
			txt_output = TotalOpenTXT(pnts, (outName+'.txt'))

        #execute parsing and exporting ops
        def goTS(self,ts,fileIn,frmt,outName):
		
           exec('from models.%s import ModelParser' % ts)
           
           main = ModelParser(open(fileIn).read())
           
           #main.parse_retrieve_data()
	   punti = main.points.list_to_tuple()
           
           Graph2D(punti)
           Graph3D(punti)
		
	   self.exportAction(frmt,punti,outName)
	

if __name__ == '__main__':
	
	Tops_ParserExport()