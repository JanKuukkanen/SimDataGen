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
	threading_is = True
	threads = None
	
	# Initialize database object
	cas_conn = DatabaseSession()

	#Constructor
	def __init__(self, id_range_start=1000, id_range_end=1010, waterlevel=30):

		self.id_range_start = id_range_start
		self.id_range_end = id_range_end
		self.waterlevel = waterlevel
		self.time = get_time_format()

	#Methods

	# Threading function
	def thread_script(self, arg):
		id_same = False
		increment = 1
		current_id = self.id_range_start

		# Get all id's from the database so we can compare them to the current id
		db_ids = self.cas_conn.fetch_ids()

		while (self.threading_is == True):
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

			# Increment waterlevel
			self.waterlevel = self.waterlevel + increment

			# Reset current_id to id_range_start
			if (current_id == self.id_range_end):
				current_id = self.id_range_start
			else:
				current_id = current_id + 1

	# Insert data into the database using an id range
	def run_by_idrange(self):
		id_same = False
		increment = 1
		current_id = self.id_range_start

		# Get all id's from the database so we can compare them to the current id
		db_ids = self.cas_conn.fetch_ids()

		while (current_id <= self.id_range_end):
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

			# Increment waterlevel
			self.waterlevel = self.waterlevel + increment

			current_id = current_id + 1

	# Threading frame
	def run_indef(self):
		try:
			# Set the target function and arguments for thread
			self.threads = Thread(target = self.thread_script, args = (1, ))

			self.threads.start()

		except Exception as e:
			print e
			sys.exit()

	# Close running thread and database connection
	def database_close(self):
		# Set threading_is variable to false so the threead will close
		self.threading_is = False
		# Close database connection
		self.cas_conn.close_connection()


	# Function called from SDG_proto
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

			if (con_success == True and runmode == 1):
				# Close connection
				self.database_close()
			
		else:
			print "Error: Failed to insert data to database!"