# Functions used for data formatting and validation

import datetime

# Format datetime to a form fitting Cassandra's datetime type
def get_time_format():
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	return time