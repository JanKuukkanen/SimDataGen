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

	print "****************************************************\n"
	print "*                                                  *\n"
	print "*                   Welcome                        *\n"
	print "*                     to                           *\n"
	print "*                 SimDataGen                       *\n"
	print "*                                                  *\n"
	print "****************************************************\n"

	while (loop != "exit"):
		option = raw_input("Enter a number to start an action:\n" + "1 to start SimDataGen test mode\n" + "2 to change delay speed\n" +
							"3 to start SimDataGen sewer system simulation\n" + "4 to start simulation animation\n" + "5 to change a location's parameter\n" +
							"0 to close the program\n" + "simdatagen>> ")

		if (option == "1"):
			sdg.start_test()

			sdg_started = True

		elif (option == "2"):
			if (sdg_started == True):
				delay_time = raw_input("Enter delay speed: ")

				print delay_time, "\n"

				sdg.set_delay_time(delay_time)
			else:
				print "SimDataGen has not been started"

		elif (option == "3"):
			sdg.start_simulation()

			sdg_started = True

		elif (option == "4"):
			if (sdg_started == True):
				sdg.run_animation()
			else:
				print "SimDataGen has not been started"

		elif (option == "5"):
			if (sdg_started == True):
				sdg.show_locations()

				selected_loc = raw_input("Choose the location you wish to alter: ")

				checkloc = sdg.check_location(selected_loc)

				sdg.show_parameters()

				selected_parameter = raw_input("Choose the parameter you wish to alter: ")

				checkpar = sdg.check_parameters(selected_parameter)

				if (checkloc == True and checkpar == True):

					sdg.change_parameter(selected_loc, selected_parameter)

					print "Location parameter('s) changed\n"

				else:
					print "Failed to change location parameter"

			else:
				print "SimDataGen has not been started"

		elif (option == "0"):
				loop = "exit"

		else:
			print "Enter a valid number!"

	connection = sdg.check_database_connection()
	if (connection == True):
		sdg.database_close()
	
	sys.exit()

except (KeyboardInterrupt, SystemExit):
	sys.exit()