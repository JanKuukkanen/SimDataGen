# SimDataGen cassandra database configuration file
import os
import sys

try:
	username = raw_input("Enter Cassandra username: ")
	password = raw_input("Enter Cassandra password: ")
	keyspace = raw_input("Enter Cassandra keyspace: ")
	node_ips = raw_input("Enter Cassandra ip-address: ")
	table = raw_input("Enter Cassandra table name: ")

	text_file = open("../src/data_file.py", "w")

	text_file.write('# File for storing information about the database.\n\n')
	text_file.write('username = "' + username + '"\n')
	text_file.write('password = "' + password + '"\n')
	text_file.write('keyspace = "' + keyspace + '"\n')
	text_file.write("node_ips = ['" + node_ips + "']\n")
	text_file.write('port = "9042"\n')
	text_file.write('table = "' + table + '"\n\n')

	text_file.write('def get_username():\n    return username\n')
	text_file.write('def get_password():\n    return password\n')
	text_file.write('def get_keyspace():\n    return keyspace\n')
	text_file.write('def get_node_ips():\n    return node_ips\n')
	text_file.write('def get_port():\n    return port\n')
	text_file.write('def get_table():\n    return table\n')

except Exception as e:
	print e