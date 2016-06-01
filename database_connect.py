from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# get metadata regarding database from a separate file
import imp
modl = imp.load_source('data_file', '/home/user/data_file.py')


class DatabaseSession(object):

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

		#Attributes
		self.username = modl.get_username()
		self.password = modl.get_password()
		self.keyspace = modl.get_keyspace()
		self.session = None
		self.connection = False
		self.node_ips = modl.get_node_ips()
		self.port = modl.get_port()
		self.metadata = None


	#methods
	def establish_connection(self):
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
			print "Error: No database connection"

	def get_connection(self):
		if (self.connection == True):
			return self.connection
		else:
			print "Error: No database connection"

	def close_connection(self):
		try:
			self.session.cluster.shutdown()
			self.session.shutdown()
			print "Connection closed"
		except Exception as e:
			print e