#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Class file for measurement locations

import math
import random

class MeterWell(object):

	#Attributes
	wellid = None
	name = None
	# Sijainti
	eastloc = None
	northloc = None
	# Kaivon sijainti merenpinnasta
	well_level = None
	# Kaivon halkaisija
	well_diameter = None
	# Virtaustilavuus (tietokannassa virtausnopeus)
	flowrate = None
	# Vedenpinta
	watersurface = None
	# Lampotila
	temperature = None
	# Ominaissahkonjohtavuus
	conductivity = None
	# Paine
	pressure = None
	# Kaivoon tulevat virtaumat
	inc_flow_well = None
	# kaivosta lähtevat virtaumat
	out_flow_well = None
	# Incoming pipe diameter
	inc_pipe_d = 160.0/1000
	# Outgoing pipe diameter
	out_pipe_d = 160.0/1000
	# Incoming pipe length (x, y) (I, P)
	inc_pipe_loc = []
	# Outgoing pipe length (x, y) (I, P)
	out_pipe_loc = []

	# Error mode
	error_mode = 0

	# Type of well
	# 1 = incoming 0.2, outgoing 0.2
	# 2 = incoming 0.2, outgoing 0.16
	# 3 = incoming 0.16, outgoing 0.2
	# 4 = incoming 0.16, outgoing 0.16
	welltype = None

	#Constructor
	def __init__(self, wellid, name="", eastloc=1.0, northloc=1.0, well_level=0.0, inc_flow_well=0, out_flow_well=0, xi=0, yi=0, xo=0, yo=0, welltype=4):

		self.wellid = wellid
		self.name = name
		self.eastloc = eastloc
		self.northloc = northloc
		self.well_level = float(well_level)
		self.flowrate = 0.0
		self.watersurface = 0.0
		self.temperature = 0.0
		self.conductivity = 0.0
		self.pressure = 0.0
		self.inc_flow_well = inc_flow_well
		self.out_flow_well = out_flow_well
		self.inc_pipe_loc.extend([xi, yi])
		self.out_pipe_loc.extend([xo, yo])
		self.well_diameter = 0.8

		self.inc_pipe_d=0.2
		self.out_pipe_d=0.2

		self.error_mode = 0

		self.welltype = welltype

	#Methods

	# Getters & Setters
	def getWellid(self):
		return self.wellid

	def getName(self):
		return self.name

	def setEastloc(self, eastloc):
		self.eastloc = eastloc

	def setNorthloc(self, northloc):
		self.northloc = northloc

	def setWellLevel(self, well_level):
		self.well_level = well_level

	def getPressure(self):
		return self.pressure

	def setOutPipeLoc(self, x, y):
		self.out_pipe_loc[0] = x
		self.out_pipe_loc[1] = y

	def setIncPipeLoc(self, x, y):
		self.inc_pipe_loc[0] = x
		self.inc_pipe_loc[1] = y

	def setIncFlowWell(self, inc_flow_well):
		self.inc_flow_well = inc_flow_well

	def setOutFlowWell(self, out_flow_well):
		self.out_flow_well = out_flow_well

	def setErrorMode(self, error):
		self.error_mode = str(error)

	# Set incoming and outgoing pipe diameters for the well according to well type
	def setPipeDiameters(self):
		if (self.welltype == 1):
			self.inc_pipe_d = 0.2
			self.out_pipe_d = 0.2

		elif (self.welltype == 2):
			self.inc_pipe_d = 0.2
			self.out_pipe_d = 0.16

		elif (self.welltype == 3):
			self.inc_pipe_d = 0.16
			self.out_pipe_d = 0.2

		elif (self.welltype == 4):
			self.inc_pipe_d = 0.16
			self.out_pipe_d = 0.16


	# Measurement calculations

	# Counting a single flowrate, ha=starting height, hb=ending height
	def virtausnopeus(self, ha, hb, x):
		v = ha - hb
		k = self.kulmaprosentti(v, x)
		if (v<0): #jos erotus on miinusmerkkistä, kyse on paineputkesta
			#return int(random.randrange(7, 13))/10
			if (0<k and 33>=k):
				return float(random.randrange(8, 9))/10
			if (33<k and 66>=k):
				return float(random.randrange(6, 7))/10
			else:
				return 0.5
		else: #jos erotus on positiivista, kyse on kaatoputkesta
			#return int(random.randrange(4, 8))/10
			if (0<k and 33>=k):
				return float(random.randrange(30, 39))/100
			if (33<k and 66>=k):
				return float(random.randrange(4, 5))/10
			else:
				return 0.6

    # Counting the angle from 90 degrees
	def kulmaprosentti(self, v, x):
		if (0>v):
			neg = -1
			pro = neg * v
			y = 90 - pro
		else:
			y = v
		z = y / x
		c = math.atan(z)
		k = math.degrees(c)
		p = k/90
		pro = p*100
		j = int(pro)
		return j

    # Calculating the distance used as a reference, Ia=x, Ib=x, Pa=y, Pb=y
	def etaisyys(self, Ia, Ib, Pa, Pb):
		I=Ia-Ib
		P=Pa-Pb
		return math.sqrt(I*I+P*P)

    # Height of the waters surface, t=time, r=diameter of the pipe, v=volume flow rate
	def pinta(self, t, r, v):
		pii = math.pi
		x = v * t
		y = pii * r * r
		h = x / y

		return h

	# Push from the well, h=height difference from the fluid surface of the highest well
	def tyonto(self):
		h = self.watersurface
		if(0<h):
			g = 9.81
			q = float(random.randrange(4, 5))/10
			y = q*g*h
			y = y*100
			x = int(math.sqrt(y))
			x = float(x)/100

			if (0.3<x):
				self.pressure = 0.3
			else:
				self.pressure = x
		else:
			self.pressure = 0.0

    #Volumetric flow rate, d=pipe diameter, v=flow velocity
	def virtaustilavuus(self, d, v):
		pii = math.pi
		z = pii*d*d*v
		return float(z)/4

	def countWaterLevel(self, t, f, fu, last):

		# Incoming pipes length
		xa = self.etaisyys(self.inc_pipe_loc[0], self.inc_pipe_loc[1], self.eastloc, self.northloc)
		xb = self.etaisyys(self.eastloc, self.northloc, self.out_pipe_loc[0], self.out_pipe_loc[1])

		a = self.well_level
		d = self.well_diameter
		c = self.inc_flow_well
		b = self.out_flow_well

		# Incoming flow to the well
		if (c == 0):
			sisaan_v = float(random.randrange(6, 8))/10
		else:
			sisaan_v = self.virtausnopeus(c,a,xa) + fu

		if (self.error_mode == "1"):
			sisaan_v = sisaan_v * 2


		tilavuus_sisaan = float(self.virtaustilavuus(self.inc_pipe_d, sisaan_v))
		# Outgoing flow from the well
		if (b > 0):
			ulos_v = self.virtausnopeus(a, b, xb)+f
			tilavuus_ulos = float(self.virtaustilavuus(self.out_pipe_d, ulos_v))

		# Water surface level
		if (b > 0):
			self.flowrate = tilavuus_sisaan - tilavuus_ulos
		else:
			self.flowrate = tilavuus_sisaan
		r = d/2
		muutos = float(self.pinta(t, r, self.flowrate))
		syvyys = self.watersurface + muutos

		if (last == True):
			if (syvyys < 0):
				self.watersurface = 0
			elif (syvyys > 0 and 2.2 >= syvyys):
				self.watersurface = syvyys
			else:
				self.watersurface = 2.2
		else:
			if (0 < syvyys):
				self.watersurface = syvyys
			else:
				self.watersurface = 0