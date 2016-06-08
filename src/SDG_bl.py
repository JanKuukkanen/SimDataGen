# SimDataGen Business logic layer

from database_connect import DatabaseSession
import sys
from threading import Thread
from time import sleep
from data_format import *

class SimDataGen(object):

	#Attributes
	id_range_start = None
	id_range_end = None
	waterlevel = None
	time = None
	threading_is = False
	threads = None
	delay_time = 60
	
	# Initialize database object
	cas_conn = DatabaseSession()

	#Constructor
	def __init__(self, id_range_start=1000, id_range_end=1010, waterlevel=30):

		self.id_range_start = id_range_start
		self.id_range_end = id_range_end
		self.waterlevel = waterlevel
		self.time = get_time_format()
		self.delay_time = 60

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

	# Threading frame
	def run_indef(self):
		try:
			# Set the target function and arguments for thread
			self.threads = Thread(target = self.thread_script, args = (1, ))

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

	# Function called from main program
	def start_sdg(self, runmode):
		# Do not allow id's below 1000 to be used
		if (self.id_range_start > 999):

			self.cas_conn.establish_connection()

			if (runmode == 1):
				self.run_by_idrange()
			elif (runmode == 2):
				self.run_indef()
			else:
				print "Logic Error: other runmodes under construction"

			con_success = self.cas_conn.get_connection()
			
		else:
			print "Logic Error: ID range too small!"