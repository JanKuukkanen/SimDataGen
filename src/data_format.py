# Functions used for data formatting and validation

import datetime
import os


# Format datetime to a form fitting Cassandra's datetime type
def getTimeFormat():
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return time

def logData(location, message, overwrite):
	try:
		dir_ = os.path.dirname(os.path.realpath("SDG_main.py"))
		if (overwrite == True):
			text_file = open(dir_ + "/log/log.txt", "w")
		else:
			text_file = open(dir_ + "/log/log.txt", "a")
		date = getTimeFormat()
		text_file.write("\n" + date + " \n " + message + " in " + location + "\n------------------------------")
		text_file.close()
	except Exception as e:
		print e
