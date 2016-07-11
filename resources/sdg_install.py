# SimDataGen cassandra database configuration file
import os
import sys

try:
	username = raw_input("Enter Cassandra username: ")
	password = raw_input("Enter Cassandra password: ")
	keyspace = raw_input("Enter Cassandra keyspace: ")
	node_ips = raw_input("Enter Cassandra ip-address: ")
	port = "9042"
	table = "measuring_data"

	text_file = open("./src/data_file.py", "w")

	text_file.write('# File for storing information about the database.\n\n')
	text_file.write('username = "' + username + '"\n')
	text_file.write('password = "' + password + '"\n')
	text_file.write('keyspace = "' + keyspace + '"\n')
	text_file.write("node_ips = ['" + node_ips + "']\n")
	text_file.write('port = "' + port + '"\n')
	text_file.write('table = "' + table + '"\n\n')

	text_file.write('def getUsername():\n    return username\n')
	text_file.write('def getPassword():\n    return password\n')
	text_file.write('def getKeyspace():\n    return keyspace\n')
	text_file.write('def getNodeIps():\n    return node_ips\n')
	text_file.write('def getPort():\n    return port\n')
	text_file.write('def getTable():\n    return table\n')

except Exception as e:
	print e