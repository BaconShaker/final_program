#!/envs/CRES/bin/python

# Use this script to check if the SQL is running. If it's not, start it
# 	if it is let it run. 

import subprocess
import time
import os

check_path = os.path.expanduser('~/GoogleDrive/all_in_one/checker.sh')
# print "Check path: ", check_path

is_on = subprocess.call([check_path])
# is_on == 0 means sql is running

class CRES_SQL(object):
	"""docstring for CRES_SQL"""
	def __init__(self):
		print "This is CRES_SQL. Making sure the SQL server is up and running."
		
		
	def is_running(self):

		

		if is_on != 0:
			try:
				os.system('open -a MAMP')
				print "MySql was not running so I started it for you."
				print "..."
				# sql_starter = os.path.expanduser('~/GoogleDrive/all_in_one/startSql.sh')
				# subprocess.call( [sql_starter] )
				# subprocess.call(['clear'])
				time.sleep(5)
			except Exception, e:
				print "*****************"
				raise e
		

		else:
			print "MySql is already running, silly goose!\n"



	def turn_off(self):
		print "Turning the SQL server off!"
		off_path = os.path.expanduser('~/GoogleDrive/all_in_one/stopSql.sh')
		subprocess.call([off_path])
		print "Done."


if __name__ == '__main__':
	a = CRES_SQL()
	a.turn_off()




