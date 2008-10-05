#!/usr/bin/env python
# -*- coding: utf-8 -*-
# filename: tops_interface.py
# Copyright 2008 Luca Bianconi<lc.bianconi@googlemail.com> and Stefano Costa <steko@iosa.it>
# Under the GNU GPL 3 License


import sys
import os.path

from models import models



class TOPS:

	def __init__(self):
		
		#to be entered maybe from a txt file containing the list of the supported models
		supportedTs = ("Zeiss_Elta_r55","Leica_Tcr_1205")
		
		supportedExportFormats=("CSV","DXF","DAT","TXT")
		
		
		try:
		
			fileToOpen = sys.argv[1]
			tsModel = sys.argv[2]
			exportFormat = sys.argv[3]
			fileToSave = sys.argv[4]
			
			
		except IndexError:
			
			print "Incorrect number of arguments: "
			print "tops_interface <fileToOpen> <TotalStationModel> <exportFormat> <OutputFile'sName>"
			
			sys.exit()
		
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
			
			#print "Input Data File not existent"
			#print "Please chose a correct file name"
			
			sys.exit("Input Data File not existent"+"\n"+"Please chose a correct file name")
		
		
		#if(tsModel == "Zeiss_Elta_r55"):
			
			#self.goZeissEltaR55(fileToOpen,exportFormat,fileToSave)
		
			
		#elif(tsModel == "Leica_Tcr_1205"):
			
			#self.goLeicaTCR1205(fileToOpen,exportFormat,fileToSave)
		if tsModel in models.models.values():
                    self.goTS(tsModel,fileToOpen,exportFormat,fileToSave)	
		else:
			print "Incorrect Total Station Model type!"
			print "Supported models are: "
			for ts in supportedTs:
				print ts
	
	
	
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
		
	#Zeiss' routine
	def goZeissEltaR55(self,fileIn,frmt,outName):
		
		from models import zeiss_elta_r55
		
		# read TS data
		
		main = zeiss_elta_r55.ModelParser(fileIn)
		punti = main.t_points
		
		codici = set([ p[4] for p in punti ])
		
		self.exportAction(frmt,punti,outName)
		
	#Leica's routine
	def goLeicaTCR1205(self,fileIn,frmt,outName):
	
		from models import leica_tcr_1205
		
		# read TS data
		
		main = leica_tcr_1205.ModelParser(fileIn)
		main.parse_retrieve_data()
		punti = main.points.list_to_tuple()
		
		self.exportAction(frmt,punti,outName)
                
        def goTS(self,ts,fileIn,frmt,outName):
		
           exec('from models.%s import ModelParser' % ts)
           
           main = ModelParser(fileIn)
           
           main.parse_retrieve_data()
	   punti = main.points.list_to_tuple()
		
	   self.exportAction(frmt,punti,outName)
	

if __name__ == '__main__':
	
	TOPS()