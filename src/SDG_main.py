# Main functionality (Presentation layer)
import os
import sys
from data_format import *

try:
	from SDG_bl import SimDataGen

	loop = None
	sdg_started = False
	error_mode = 0

	dir_ = os.path.dirname(os.path.realpath("SDG_main.py"))
	if not os.path.lexists(dir_ + "/log"):
		os.makedirs(dir_ + "/log")
		os.chmod(dir_ + "/log", 0777)

	# Initialize SimDataGen object
	sdg = SimDataGen(5)

	print "****************************************************\n"
	print "*                                                  *\n"
	print "*                   Welcome                        *\n"
	print "*                     to                           *\n"
	print "*                 SimDataGen                       *\n"
	print "*                                                  *\n"
	print "****************************************************\n"

	while (loop != "exit"):
		option = raw_input("Enter a number to start an action:\n" + "1 to change delay speed\n" +
							"2 to start SimDataGen sewer system simulation\n" + "3 to start simulation animation\n" + "4 to change a location's parameter\n" +
							"5 to add a new location\n" + "6 to clear extra wells\n" + "7 to display currently existing well locations\n" +
							"8 to enable error mode\n" + "9 to disable error mode\n" + "0 to close the program\n" + "simdatagen>> ")


		# Alter program's updating delay amount
		if (option == "1"):
			if (sdg_started == True):
				delay_time = raw_input("Enter delay speed: ")

				validate_delay = sdg.validateDelayTime(delay_time)

				if (validate_delay == True):
					print delay_time, "\n"
					sdg.setDelayTime(delay_time)

				else:
					print "You have entered an invalid input!"
			else:
				print "SimDataGen has not been started"

		# Start 10 well location simulation
		elif (option == "2"):
			sdg.startSimulation()

			sdg_started = True

		# Start mathplotlib visualization of the database traffic
		elif (option == "3"):
			if (sdg_started == True):
				sdg.runAnimation()
			else:
				print "SimDataGen has not been started"

		# Alter a specific well's parameters
		elif (option == "4"):
			if (sdg_started == True):
				sdg.showLocations()

				selected_loc = raw_input("Choose the location you wish to alter: ")

				checkloc = sdg.checkLocation(selected_loc)

				sdg.showParameters()

				selected_parameter = raw_input("Choose the parameter you wish to alter: ")

				checkpar = sdg.checkParameters(selected_parameter)

				if (checkloc == True and checkpar == True):

					sdg.changeParameter(selected_loc, selected_parameter)

					print "Location parameter('s) changed\n"

				else:
					print "Failed to change location parameter"

			else:
				print "SimDataGen has not been started"

		# Add a new well with custom information
		elif (option == "5"):
			if (sdg_started == True):
				answers = [None] * 10
				contadd = True

				# Ask the user for the parameters the well will use and set them to be the right type. No user input validation currently
				eastloc = raw_input("Enter east location: ")
				answers[1] = int(eastloc)

				northloc = raw_input("Enter north location: ")
				answers[2] = int(northloc)

				well_level = raw_input("Enter well level: ")
				answers[3] = float(well_level)

				incflow = raw_input("Enter incoming well level: ")
				answers[4] = int(incflow)

				outflow = raw_input("Enter outgoing well level: ")
				answers[5] = int(outflow)

				incflowE = raw_input("Enter incoming well east location: ")
				answers[6] = int(incflowE)

				incflowN = raw_input("Enter incoming well north location: ")
				answers[7] = int(incflowN)

				outflowE = raw_input("Enter outgoing well east location: ")
				answers[8] = int(outflowE)

				outflowN = raw_input("Enter outgoing well north location: ")
				answers[9] = int(outflowN)

				well_type = raw_input("Enter well type: ")
				answers[0] = int(well_type)

				sdg.addNewWell(answers[1], answers[2], answers[3], answers[4], answers[5], answers[6], answers[7], answers[8], answers[9], answers[0])

			else:
				print "SimDataGen has not been started"

		# Clear custom parameter wells
		elif (option == "6"):
			if (sdg_started == True):
				sdg.clearWells()
			else:
				print "SimDataGen has not been started"

		# Display currently existing wells and ask if the user would like to have detailed inforation on a specific one
		elif (option == "7"):
			if (sdg_started == True):
				loop_continue = True

				sdg.displayLocations()

				while (loop_continue == True):

					spec_well = raw_input("Enter a location name to display further information or enter 0 to exit: ")

					namematch = sdg.checkNameInput(spec_well)

					if (namematch == True):
						sdg.displayWell(spec_well)

					elif (spec_well == "0"):
						print "No location selected"
						loop_continue = False

					else:
						print "Enter a valid location name!"

			else:
				print "SimDataGen has not been started"

		# Enable error mode by asking the user which error to use, currently only overflow error is supported
		elif (option == "8"):
			if (sdg_started == True):
				
				sdg.displayLocations()

				errwell = raw_input("Enter the number of the well you would like the error to take place in: ")

				print "1. Overflow error"

				error = raw_input("Enter which error you would like to enable: ")

				sdg.enableError(errwell, error)

				error_mode = 1

				print "Error mode enabled\n"

			else:
				print "SimDataGen has not been started"

		elif (option == "9"):
			if (sdg_started == True and error_mode == 1):
				sdg.disableErrors()

				error_mode = 0

				print "Error mode disabled\n"

			else:
				print "SimDataGen has not been started or error mode is not enabled"

		elif (option == "0"):
				loop = "exit"

		else:
			print "Enter a valid number!"

	connection = sdg.checkDatabaseConnection()
	if (connection == True):
		sdg.databaseClose()
	
	sys.exit()

except Exception, e:
	logData("SDG_main/imports", str(e), False)
	print "Failed to Start SimDataGen! Make sure you have a working Cassandra database with the correct sql schema created. " \
			"The database schema can be found in the resources folder. After you have the database working run the installation_sdg.sh file"
	sys.exit