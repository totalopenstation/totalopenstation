#! /usr/bin/env python

from sdxf import *

class Tops_Dxf:
	
	def __init__(self, tuplepoints, filename):
	
		self.points = tuplepoints
		self.codes = self.make_codes(self.points)
		self.filename = filename
		self.dxf_doc = self.createDxf(self.codes,self.points)
		self.export_Dxf_ToFile(self.dxf_doc,self.filename)
		
	def make_codes(self, points):
		
		codes = set([ p[4] for p in points])
		
		return codes
	
	def createDxf(self, codes, points):
		
		#Drawing
		d=Drawing(layers=())
		#tables
		d.styles.append(Style())                #table styles
		#d.styles.append(Style( name='GQB', height=0.04 ))
		d.views.append(View('Normal'))          #table view
		d.views.append(ViewByWindow('Window',leftBottom=(1,0),rightTop=(2,1)))  #idem
		
		for n, i in enumerate(codes):
			name_p = "%s_PUNTI" % i
			name_q = "%s_QUOTE" % i
			name_n = "%s_NUMERI" % i
			d.append(Layer(name=name_p, color=n))
			d.append(Layer(name=name_q, color=n))
			d.append(Layer(name=name_n, color=n))
		
		for p in points:
			p_id, p_x, p_y, p_z, p_layer = p
		
		if p_layer < 1200:
			
			name_p = "%s_PUNTI" % p_layer
			name_q = "%s_QUOTE" % p_layer
			name_n = "%s_NUMERI" % p_layer
			
			# add point
			d.append(Point(points=[(p_x, p_y, 0)], layer=name_p, color=256))
			
			# add ID number
			d.append(Text(str(p_id),point=(p_x, p_y, 0), layer=name_n ))
			
			# add Z value
			d.append(Text(str(p_z), point=(p_x, p_y, 0), layer=name_q ))
		
		return d
		
	def export_Dxf_ToFile(self, dxf, filename):
		
		dxf.saveas(filename)
