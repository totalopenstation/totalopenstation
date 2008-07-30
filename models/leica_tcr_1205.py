#!/usr/bin/env python

class Point:
	
	def __init__(self, p_id, text, x, y, z):
		self.p_id= p_id
		self.text=text
		self.x=x
		self.y=y
		self.z=z
		
	def get_coords(self):
		
		self.coords = {'x': self.x,'y':self.y,'z':self.z}
		return self.coords
	
	def dump_point(self):
		
		print self.p_id," ",self.x," ",self.y," ",self.z

class PointsList:
	
	def __init__(self):
		
		self.listofpoints = []
		
	def add_point(self, p):
		
		self.listofpoints.append(p)
		
	def add_points(self, lp):
		
		self.listofpoints.extend(lp)
		
	def pid_is_in_lop(self, aux_p_id):
		
		for p in self.listofpoints:
			
			if aux_p_id == p.p_id :
				return True
		
		return False

class Data:
	
	def _init_(self):
		self.lines
		
	def data_from_txt_file(self, filepathname):
		
		file = open(filepathname)
		self.lines = file.readlines()

class TotalStation:
	
	def __init__(self,filename):
		
		self.d = Data()
		self.d.data_from_txt_file(filename)
		self.points = PointsList()
		
	def set_data(self, data):
		
		self.d= data
	
	def get_data(self):
		
		return self.d
	
	def parse_retrieve_data(self):
		
		valid_lines = filter(self.is_point, self.d.lines)
		
		for l in valid_lines:

			self.points.add_point(self.get_point(l))
	
	def is_point(self):
		pass
	
	def get_point(self):
		pass
	
	def print_found_points(self):
		
		for p in self.points.listofpoints:
			p.dump_point()


class ZeissEltaR55(TotalStation):
	
	def is_point(self,line):
		
		tokens = line.split()
		
		try:
			int(tokens[0])
			int(tokens[1])
			float(tokens[3])
			float(tokens[5])
			float(tokens[7])
		
		except (ValueError, IndexError):
			
			is_point = False
		
		else:
			
			is_point = True
		
		return is_point
	
	def get_point(self,line):
		
		tokens = line.split()
		
		p = Point(int(tokens[1]), "", float(tokens[3]), float(tokens[5]), float(tokens[7]))
		
		return p


class LeicaTCR1205(TotalStation):
	
	def parse_retrieve_data(self):
		
		valid_lines = []
		
		for l in self.d.lines:
			
			if l.startswith('FEA'):
				if self.is_point(l) == True:
					
					valid_lines.append(l)

		for l in valid_lines:

			aux = self.get_point(l)
			
			if (self.points.pid_is_in_lop(aux.p_id)) == False :
				
				self.points.add_point(aux)
	
	def is_point(self,line):
		
		tokens = line.split()
		
		try:
			str(tokens[0])
			float(tokens[1])
			float(tokens[2])
			float(tokens[3])
		
		except (ValueError, IndexError):
			
			is_point = False
		
		else:
			
			is_point = True
		
		return is_point
		
	def get_point(self,line):
		
		tokens = line.split()
		
		p = Point(str(tokens[0]), "", float(tokens[1]), float(tokens[2]), float(tokens[3]))
		
		return p


class Tops:
	
	print "This is your new Total Open StationS"
	print "by Iosa's team"
	
	testZ = ZeissEltaR55('zeiss_elta_r55')
	testZ.parse_retrieve_data()
	testZ.print_found_points()
	
	testL = LeicaTCR1205('leica 1205.txt')
	testL.parse_retrieve_data()
	testL.print_found_points()
	
	
#if __name__ == "__main__":
#	main = Tops()
