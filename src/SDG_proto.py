<<<<<<< HEAD
# Main functionality (Presentation layer)

from SDG_bl import SimDataGen
import sys

try:
	loop = None

	answer = raw_input("Enter thread number: ")

	if (answer == "1"):
		# Initialize SimDataGen object
		sdg = SimDataGen(1000, 1019, 30)

		sdg.start_sdg(2)

	elif (answer == "2"):
		sdg = SimDataGen(1010, 1010, 30)

		sdg.start_sdg(2)

	while (loop != "exit"):
		option = raw_input("Enter 1 to change delay speed or enter 0 to close the program: ")

		if (option == "1"):
			delay_time = raw_input("Enter delay speed: ")

			print delay_time, "\n"

			sdg.set_delay_time(delay_time)

		elif (option == "0"):
			loop = "exit"

	sdg.database_close()
	
	sys.exit()

except (KeyboardInterrupt, SystemExit):
	sys.exit()
=======
from database_connect import DatabaseSession

# initialize database object
tmp_conn = DatabaseSession()

# Connect to database
tmp_conn.establish_connection()

con_success = tmp_conn.get_connection()

if (con_success == True):
	
	tmp_conn.send_current(1000, 1010)

	tmp_conn.close_connection()
>>>>>>> upstream/master
