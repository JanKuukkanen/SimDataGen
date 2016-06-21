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
	def __init__(self, uname="", pword="", kspace="", _node_ips="", _port=""):

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

	def fetch_ids(self):
		if (self.connection == True):
			try:
				table = modl.get_table()

				db_ids = self.session.execute('SELECT id FROM ' + table)
				return db_ids
			except Exception, e:
				print "Database Error: ", e

	def fetch_watersurface(self):
		if (self.connection == True):
			try:
				table = modl.get_table()

				watersurfaces = self.session.execute('SELECT vedenpinta FROM ' + table)
				return watersurfaces

			except Exception as e:
				print "Database Error: ", e

	def fetch_rowcount(self):
		if (self.connection == True):
			try:
				table = modl.get_table()

				rows = self.session.execute('SELECT COUNT(*) FROM ' + table)

				return rows[0]

			except Exception as e:
				print "Database Error: ", e

	def fetch_name(self):
		if (self.connection == True):
			try:
				table = modl.get_table()

				names = self.session.execute('SELECT nimi FROM ' + table)
				return names
				
			except Exception as e:
				print "Database Error: ", e

	def delete_row(self, c_id):
		try:
			table = modl.get_table()
			delid = c_id

			if (self.connection == True):
				self.session.execute("DELETE FROM " + table + " WHERE id = " + delid + " IF EXISTS")
			else:
				print "Database Error: Failed to delete data in the database!"

		except Exception as e:
			print e

	def send_meterwell_data(self, id_same, c_id, nimi, east, north, korkeus_merenpinnasta, lampotila, ominaissahkojohtavuus, paine, vedenpinta, virtausnopeus):
		if (self.connection == True):
			try:
				table = modl.get_table()

				# Update row if current id already exists or insert new id if it does not
				if (id_same == True):
					self.session.execute("UPDATE " + table + " SET nimi = (%s), east = (%s), north = (%s), korkeus_merenpinnasta = (%s), lampotila = (%s), ominaissahkojohtavuus = (%s), paine = (%s), vedenpinta = (%s), virtausnopeus = (%s) WHERE id = (%s)", (nimi, east, north, korkeus_merenpinnasta, lampotila, ominaissahkojohtavuus, paine, vedenpinta, virtausnopeus, c_id))
				elif (id_same == False):
					self.session.execute("INSERT INTO " + table + " (id, nimi, east, north, korkeus_merenpinnasta, lampotila, ominaissahkojohtavuus, paine, vedenpinta, virtausnopeus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (c_id, nimi, east, north, korkeus_merenpinnasta, lampotila, ominaissahkojohtavuus, paine, vedenpinta, virtausnopeus))
				else:
					print "Database Error: Somethin's gone all wrong"

			except Exception as e:
				print e
		else:
			print "Database Error: Failed to insert data to database!"

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