# Functions used for data formatting and validation

import datetime
import os


# Format datetime to a form fitting Cassandra's datetime type
def get_time_format():
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return time

def log_data(location, message, overwrite):
	try:
		dir_ = os.path.dirname(os.path.realpath("SDG_main.py"))
		if (overwrite == True):
			text_file = open(dir_ + "/log/log.txt", "w")
		else:
			text_file = open(dir_ + "/log/log.txt", "a")
		date = get_time_format()
		text_file.write("\n" + date + " \n " + message + " in " + location + "\n------------------------------")
		text_file.close()
	except Exception as e:
		print e
