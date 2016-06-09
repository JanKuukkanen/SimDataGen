# Main functionality (Presentation layer)

from SDG_bl import SimDataGen
import os
import sys

try:
	loop = None
	sdg_started = False

	if not os.path.lexists("/var/log/SimDataGen"):
		os.makedirs("/var/log/SimDataGen")

	# Initialize SimDataGen object
	sdg = SimDataGen(10)

	while (loop != "exit"):
		option = raw_input("Enter 1 to start SimDataGen, 2 to change delay speed or enter 0 to close the program: ")

		if (option == "1"):
			sdg.start_sdg()

			sdg_started = True

		elif (option == "2"):
			if (sdg_started == True):
				delay_time = raw_input("Enter delay speed: ")

				print delay_time, "\n"

				sdg.set_delay_time(delay_time)
			else:
				print "SimDataGen has not been started"

		elif (option == "0"):
			if (sdg_started == True):
				loop = "exit"
			else:
				print "SimDataGen has not been started"

	sdg.database_close()
	
	sys.exit()

except (KeyboardInterrupt, SystemExit):
	sys.exit()