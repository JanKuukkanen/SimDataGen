# Functions used for data formatting and validation

import datetime


# Format datetime to a form fitting Cassandra's datetime type
def get_time_format():
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return time

def log_data(location, message):
	text_file = open("/var/log/SimDataGen/log.txt", "a")
	date = get_time_format()
	text_file.write("\n" + date + " \n " + message + " in " + location + "\n------------------------------")
	text_file.close()
