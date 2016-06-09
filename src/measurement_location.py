

class MeterWell(object):

	#Attributes
	wellid = None
	parent = None
	name = None
	eastloc = None
	northloc = None
	waterlevelheight = None
	flowrate = None
	watersurface = None
	temperature = None
	conductivity = None
	pressure = None

	#Constructor
	def __init__(self, wellid, parent=1, name="", eastloc="", northloc="", waterlevelheight="", flowrate="", watersurface="", temperature="", conductivity="", pressure=""):

		self.wellid = wellid
		self.parent = parent
		self.name = name
		self.eastloc = eastloc
		self.northloc = northloc
		self.waterlevelheight = waterlevelheight
		self.flowrate = flowrate
		self.watersurface = watersurface
		self.temperature = temperature
		self.conductivity = conductivity
		self.pressure = pressure

	#Methods

	# Getters & Setters
	def get_name(self):
		return self.name

	def set_name(self, name):
		self.name = name

	def get_eastloc(self):
		return self.eastloc

	def set_eastloc(self, eastloc):
		self.eastloc = eastloc

	def get_northloc(self):
		return self.northloc

	def set_northloc(self, northloc):
		self.northloc = northloc

	def get_waterlevelheight(self):
		return self.waterlevelheight

	def set_waterlevelheight(self, waterlevelheight):
		self.waterlevelheight = waterlevelheight

	def get_flowrate(self):
		return self.flowrate

	def set_flowrate(self, flowrate):
		self.flowrate = flowrate

	def get_watersurface(self):
		return self.watersurface

	def set_watersurface(self, watersurface):
		self.watersurface = watersurface

	def get_temperature(self):
		return self.temperature

	def set_temperature(self, temperature):
		self.temperature = temperature

	def get_conductivity(self):
		return self.conductivity

	def set_conductivity(self, conductivity):
		self.conductivity = conductivity

	def get_pressure(self):
		return self.pressure

	def set_pressure(self, pressure):
		self.pressure = pressure

	# Measurement calculations