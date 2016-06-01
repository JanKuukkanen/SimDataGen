import datetime

def get_time_format():
	time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

	return time