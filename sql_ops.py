#!/Users/AsianCheddar/GoogleDrive/all_in_one/bin/python

# Use this script to check if the SQL is running. If it's not, start it
# 	if it is let it run. 

import subprocess
import time
import os




is_on = subprocess.call(['/Users/AsianCheddar/GoogleDrive/all_in_one/checker.sh'])
# is_on == 0 means sql is running

class CRES_SQL(object):
	"""docstring for CRES_SQL"""
	def __init__(self):
		print "Hello There"
		
		
	def is_running(self):

		

		if is_on != 0:

			os.system('open -a MAMP')
			print "MySql was not running so I started it for you."
			print ""
			# subprocess.call( ['/Users/AsianCheddar/GoogleDrive/all_in_one/startSql.sh'] )
			# subprocess.call(['clear'])
			time.sleep(3)


		else:
			print "MySql is already running, silly goose!\n"



	def turn_off(self):
		print "Turning the SQL server off!"
		subprocess.call(['/Users/AsianCheddar/GoogleDrive/all_in_one/stopSql.sh'])







