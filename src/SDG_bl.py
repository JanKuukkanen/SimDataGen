# SimDataGen Business logic layer

from database_connect import DatabaseSession
from measurement_location import MeterWell
import sys
from threading import Thread
from time import sleep
from data_format import *

class SimDataGen(object):

	#Attributes
	time = None
	threading_is = False
	threads = None
	delay_time = 60
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
					log_data("SDG_bl/thread_script", "Inserted data into database")
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
		current_id = self.locationList[0].get_wellid()

		# Get all id's from the database so we can compare them to the current id
		db_ids = self.cas_conn.fetch_ids()

		self.threading_is = True

		while (self.threading_is == True):

			# Suspend execution for 5 seconds
			sleep(self.delay_time)

			# Check if our current id already exists in the database
			for user_id in db_ids:
				if (current_id == user_id):
					id_same = True
				else:
					id_same = False

			self.time = get_time_format()

			self.cas_conn.send_meterwell_data(id_same, current_id, self.locationList[0].name, self.locationList[0].eastloc, self.locationList[0].northloc, self.locationList[0].waterlevelheight, self.locationList[0].temperature, self.locationList[0].conductivity, self.locationList[0].pressure, self.locationList[0].watersurface, self.locationList[0].flowrate)

			try:
				log_data("SDG_bl/thread_script", "Inserted data into database")
			except Exception, e:
				print e

	# Threading frame
	def thread_init(self):
		try:
			# Set the target function and arguments for thread
			self.threads = Thread(target = self.meterwell_thread, args = (1, ))

			self.threads.start()

			try:
				log_data("SDG_bl/run_indef", "Started thread")
			except Exception, e:
				print e

		except Exception as e:
			print e
			sys.exit()

	# Close running thread and database connection
	def database_close(self):
		# Set threading_is variable to false so the thread will close
		self.threading_is = False

		# Wait for active threads to finish
		self.threads.join()
		# Close database connection
		self.cas_conn.close_connection()

		try:
			log_data("SDG_bl/database_close", "Closed database")
		except Exception, e:
			print e

	def set_delay_time(self, delay_time):
		
		self.delay_time = int(delay_time)
		try:
			log_data("SDG_bl/set_delay_time", "Altered delay time")
		except Exception, e:
			print e

	# Function called from SDG_main
	def start_sdg(self):

		# Connect to database
		self.cas_conn.establish_connection()

		self.locationList.append(MeterWell(1, 1, "test", 1, 1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1))

		self.thread_init()

		con_success = self.cas_conn.get_connection()