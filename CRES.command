#!/envs/CRES/bin/python

# This is the MAIN PAGE for the CRES Program.

# Functionality should include:
# 	Building a pickup route
# 		Run the route
# 		Add Data to CSV files
# 		Send pickup notices/reciepts 
# 			prior to pickup? 
# 			post collection results
# 	Browsing client/location details/statistics
# 		Provide to website?




# Cheating...
mods = 1
while mods == 1:
	try:
		# IMPORT the built-in functions first so we can handle
		# errors. 
		import os.path
		import sys
		import os
		import time
		import subprocess

		# Check if the database is up and running. 
		from sql_ops import *
		check_sql = CRES_SQL()
		check_sql.is_running()

		from tabulate import tabulate #makes the nice tables
		import time #this is for any delays I want
		import urllib
		import urllib2
		from bs4 import BeautifulSoup           # pip install BeautifulS
		from datetime import date
		import thread
		# main_manipulator has Data_Manager()
		from main_manipulator import *
		from route_handler import *

		mods = 0
		

	except ImportError as err:
		print "You don't have all the required modules on this computer."
		print "ERROR: ", err, "\n"
		print  err.args

		installer = os.path.expanduser('~/GoogleDrive/all_in_one/install.command')
		subprocess.call(['sudo', installer])

		print '\n\n\nIF YOU SEE THIS GOING IN A LOOP, HIT CTRL + OPTION + "C"\n\n\n'
		time.sleep(5)
		# updater = os.path.expanduser('~/GoogleDrive/all_in_one/update.command')
		# subprocess.call([updater])
		
		print "******	******	******"
		print '\n' * 3
		print "Done updating pip. \nIf you're still getting an error, the problem is with GoogleDrive."
		print "Hit control + option + 'c' to exit. Or just close the window."
		print "******	******	******"

	print "\n***************\nthis is outside the try and except but inside the while "



def main():
	

	# Now that all the modules are in place, create a database instance 
	# and pass it the proper config details from the config file. 


	database_main = Data_Manager()

	route = Route_Manager(database_main)
	collection_list = route.run_route() # LIST OF Collection instances

	

	route.add_collections_to_db(collection_list)


	# build() needs to return something in the form of:
	# [ stop number, name, address, city, zip, contact email, phone number, 
	# 	contact name, date, charity, average donation, notes ]



if __name__ == '__main__':
	main()



