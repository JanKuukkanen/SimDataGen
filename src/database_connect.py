from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from data_format import *

# get metadata regarding database from a separate file
import imp
modl = imp.load_source('data_file', '/home/user/data_file.py')


class DatabaseSession(object):

	#Attributes
	username = None
	password = None
	keyspace = None
	session = None
	connection = False
	node_ips = None
	port = None
	metadata = None

	#Constructor
	def __init__(self="", uname="", pword="", kspace="", _node_ips="", _port=""):

		self.username = modl.get_username()
		self.password = modl.get_password()
		self.keyspace = modl.get_keyspace()
		self.session = None
		self.connection = False
		self.node_ips = modl.get_node_ips()
		self.port = modl.get_port()
		self.metadata = None


	#Methods
	# Connect to the database and set connection to true
	def establish_connection(self):
		if (self.connection == False):
			try:
				auth_provider = PlainTextAuthProvider(username = self.username, password = self.password)

				cluster = Cluster(self.node_ips, auth_provider = auth_provider, port = self.port)
				self.metadata = cluster.metadata

				self.session = cluster.connect(self.keyspace)
				print "Connected to cluster: " + self.metadata.cluster_name
				print self.session
				self.connection = True

			except Exception, e:
				print e
		else:
			print "Error: Connection already established!"

	# Test method for getting waterlevel data from the database
	def fetch_waterlevel(self):
		if (self.connection == True):
			try:
				table = modl.get_table()
				rows = self.session.execute('SELECT waterlevel FROM ' + table)
				for user_row in rows:
					print user_row.waterlevel
			except Exception as e:
				print e
		else:
			print "Error: No database connection!"

	# Insert or update data regarding the water current to the database
	def send_current(self, id_range_start, id_range_end):
		# do not allow id's below 1000 to be used
		if (self.connection == True and id_range_start > 999):
			try:
				id_same = False
				table = modl.get_table()
				current_id = id_range_start
				waterlevel = 30
				increment = 1
				time = ""

				# Get all id's from the database so we can compare them to the current id
				db_ids = self.session.execute('SELECT id FROM ' + table)

				while (current_id <= id_range_end):
					# Check if we should increase or decrease waterlevel to create a wave
					if (waterlevel == 30):
						increment = 1
					elif (waterlevel == 40):
						increment = -1

					# Check if our current id already exists in the database
					for user_id in db_ids:
						if (current_id == user_id):
							id_same = True
						else:
							id_same = False

					fetched_time = get_time_format()

					# Update row if current id already exists or insert new id if it does not
					if (id_same == True):
						self.session.execute("UPDATE " + table +" SET waterlevel = (%s), time = (%s) WHERE id = (%s)",(table, waterlevel, fetched_time, current_id))
					elif (id_same == False):
						self.session.execute("INSERT INTO " + table + " (id, time, waterlevel) VALUES (%s, %s, %s)", (current_id, fetched_time, waterlevel))
					else:
						print "Error: Something has gone terribly wrong"

					waterlevel = waterlevel + increment

					current_id = current_id + 1

			except Exception as e:
				print e
		else:
			print "Error: Failed to insert data to database!"

	# return the state of the database connection
	def get_connection(self):
			return self.connection

	# Close the database connection and set connection to false
	def close_connection(self):
		if (self.connection == True):
			try:
				self.session.cluster.shutdown()
				self.session.shutdown()
				self.connection = False
				print "Connection closed"
			except Exception as e:
				print e
		else:
			print "Error: Failed to close database connection"