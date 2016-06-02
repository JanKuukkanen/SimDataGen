# Main functionality (Presentation layer)

from SDG_bl import SimDataGen
import sys

try:
	
	# Initialize SimDataGen object
	sdg = SimDataGen(1000, 1010, 30)

	sdg.start_sdg(2)

	var = raw_input("Enter something: ")

	sdg.database_close()

except (KeyboardInterrupt, SystemExit):
	sys.exit()