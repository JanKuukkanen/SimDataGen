# SimDataGen Business logic layer

from database_connect import DatabaseSession
from measurement_location import MeterWell
import sys
from threading import Thread
from time import sleep
from data_format import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class SimDataGen(object):

	#Attributes
	time = None
	threading_is = False
	threads = None
	delay_time = 1
	locationList = []
	
	# Initialize database object
	cas_conn = DatabaseSession()

	#Constructor
	def __init__(self, delay_time=60):

		self.time = get_time_format()
		self.delay_time = delay_time
		self.locationList = []

	#Methods

	# Threading function
	def thread_script(self, arg):
		id_same = False
		increment = 1
		current_id = self.id_range_start

		# Get all id's from the database so we can compare them to the current id
		db_ids = self.cas_conn.fetch_ids()

		self.threading_is = True

		while (self.threading_is == True):

			delay_done = False
			# Suspend execution for 5 seconds
			sleep(self.delay_time)

			current_id = self.id_range_start

			while (delay_done == False):
				# Check if we should increase or decrease waterlevel to create a wave
				if (self.waterlevel == 30):
					increment = 1
				elif (self.waterlevel == 40):
					increment = -1

				# Check if our current id already exists in the database
				for user_id in db_ids:
					if (current_id == user_id):
						id_same = True
					else:
						id_same = False

				self.time = get_time_format()

				self.cas_conn.send_current(id_same, current_id, self.waterlevel, self.time)

				try:
					log_data("SDG_bl/thread_script", "Inserted data into database", False)
				except Exception, e:
					print e

				# Increment waterlevel
				self.waterlevel = self.waterlevel + increment

				# End inner loop if current_id is at the end of the id range
				if (current_id == self.id_range_end):
					delay_done = True
				else:
					current_id = current_id + 1

	# Threading function
	def meterwell_thread(self, arg):
		id_same = False
		i = 0

		# Get all id's from the database so we can compare them to the current id
		db_ids = self.cas_conn.fetch_ids()

		self.threading_is = True

		while (self.threading_is == True):

			# Suspend execution for 5 seconds
			sleep(self.delay_time)

			i = 0

			while (i < len(self.locationList)):

				current_id = self.locationList[i].get_wellid()

				# Check if our current id already exists in the database
				for user_id in db_ids:
					if (current_id == user_id):
						id_same = True
					else:
						id_same = False

				self.time = get_time_format()

				self.cas_conn.send_meterwell_data(id_same, current_id, self.locationList[i].name, self.locationList[i].eastloc, self.locationList[i].northloc, self.locationList[i].well_level, self.locationList[i].temperature, self.locationList[i].conductivity, self.locationList[i].pressure, self.locationList[i].watersurface, self.locationList[i].flowrate)

				try:
					log_data("SDG_bl/thread_script", "Inserted data into database", False)
				except Exception, e:
					print e

				i = i + 1

	# Threading frame
	def thread_init(self):
		try:
			# Set the target function and arguments for thread
			self.threads = Thread(target = self.meterwell_thread, args = (1, ))

			self.threads.start()

			try:
				log_data("SDG_bl/run_indef", "Started thread", False)
			except Exception, e:
				print e

		except Exception as e:
			print e
			sys.exit()

	# Close running thread and database connection
	def database_close(self):
		if (self.threading_is == True):
			# Set threading_is variable to false so the thread will close
			self.threading_is = False

			# Wait for active threads to finish
			self.threads.join()
		# Close database connection
		self.cas_conn.close_connection()

		try:
			log_data("SDG_bl/database_close", "Closed database", False)
		except Exception, e:
			print e

	def set_delay_time(self, delay_time):
		
		self.delay_time = int(delay_time)
		try:
			log_data("SDG_bl/set_delay_time", "Altered delay time", False)
		except Exception, e:
			print e

	def check_database_connection(self):
		connection = self.cas_conn.get_connection()
		
		return connection

	# Function called from SDG_main
	def start_test(self):

		# Connect to database
		self.cas_conn.establish_connection()

		self.locationList.append(MeterWell(0, "test", 1, 1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1))

		try:
			log_data("SDG_bl/start_test", "Simulation test started", True)
		except Exception, e:
			print e

		self.thread_init()

		con_success = self.cas_conn.get_connection()

	# Function for starting the simulation for 10 different measurement wells
	def start_simulation(self):

		# Connect to database
		self.cas_conn.establish_connection()

		# Create 10 wells with required data (id, name, east, north, well level, incoming flow to the well, outgoing flow to the well, incoming east location,
		# incoming north location, outgoing east location, outgoing north location)
		self.locationList.append(MeterWell(1, "loc-1", 0, 5, 1, 0, 5, 0, 0, 4, 3))
		self.locationList.append(MeterWell(10, "loc-2", 4, 3, 5, 1, 4, 0, 5, 7, 3))
		self.locationList.append(MeterWell(20, "loc-3", 7, 3, 4, 5, 3, 4, 3, 12, 6))
		self.locationList.append(MeterWell(30, "loc-4", 12, 6, 3, 4, 2, 7, 3, 19, 9))
		self.locationList.append(MeterWell(40, "loc-5", 19, 9, 2, 3, 1, 12, 6, 22, 10))
		self.locationList.append(MeterWell(50, "loc-6", 22, 10, 1, 2, 2, 19, 9, 23, 5))
		self.locationList.append(MeterWell(60, "loc-7", 23, 5, 2, 1, 4, 22, 10, 34, 0))
		self.locationList.append(MeterWell(70, "loc-8", 34, 0, 4, 2, 3, 23, 5, 36, 0))
		self.locationList.append(MeterWell(80, "loc-9", 36, 0, 3, 4, 5, 34, 0, 51, 7))
		self.locationList.append(MeterWell(90, "loc-10", 51, 7, 6, 3, 0, 36, 0, 0, 0))

		try:
			log_data("SDG_bl/start_simulation", "Added 10 locations", True)
		except Exception, e:
			print e

		self.thread_init()