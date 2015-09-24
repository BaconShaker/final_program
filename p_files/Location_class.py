#!/envs/CRES/bin/python
import os
import mysql.connector
from datetime import *
import numpy
import math
from __init__ import __sql_robby__, __sql__
from main_manipulator import *
from errors import *
from attrdict import AttrDict
from main_manipulator import *
from tabulate import tabulate



# Set today, this month and last month variables.
today = datetime.now()
this_month = calendar.month_name[today.month]
last_month = calendar.month_name[today.month - 1]


if os.environ['USER'] == "AsianCheddar":
	
	# Establish connection to SQL server.
	db = mysql.connector.connect(**__sql_robby__)
	cursor = db.cursor()
	print "Logged in as Robby\n"


	
else:
	
	# Establish connection to SQL server.
	db = mysql.connector.connect(**__sql__)
	cursor = db.cursor()
	print "Logged in as Mike\n"





def name_lookup(name):
	cursor.execute(
		"""Select *
			From `Locations`
			Where
				`Name` = "%s" """ % (name)
	)
	try:
		data = cursor.fetchall()[0]
		return data
	except IndexError:
		raise NoNameMatch
		
	

		
def columns(tablename):
	cursor.execute(
		"""describe %s""" % tablename
	)
	cols = [x[0].replace(" ", "_").lower() for x in cursor.fetchall() ]
	
	return cols







def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)




    

class Location(AttrDict):
	def __init__(self, name):

		zipped = zip(columns("Locations"), name_lookup(name))
		loc_dict = {k:v for k,v in zipped}
		
		AttrDict.__init__(self, loc_dict)
		print self.charity




	def pickup_lines(self, start = '01/01/2015', stop = today.date() , days = False):
		# This function should return all the pickup data for Location between specified dates.
		try:
			start_date = datetime.strptime(start, "%m/%d/%y")
		except ValueError:
			print "Start date was not in the correct format"
			start_date = datetime.strptime(start, "%m/%d/%Y")

		start_date = start_date.date()
		
		try:
			print "stop is a : ", type(stop)
			stop_date = datetime.strptime(stop, '%m/%d/%Y')
			stop_date = stop_date.date()
			
				
		except:
			print "Timer"
			stop_date = stop
			
		
		
		print '\nLooking up all pickups from' , start_date, "to", stop_date, '\n'
		cursor.execute(
			"""SELECT * FROM  `Pickups` WHERE `Location` = '%s' and `Pickup Date` between '%s' and '%s' """ % (self.name, start_date , stop_date)
		)
		picks = cursor.fetchall()
		
		
		return picks 


		
			
if __name__ == "__main__":

	
	name = "Erie Cafe"
	
	# Location([name as string])
	ro = Location(name)
	
	#	Available functions:
	#		pickup_lines(start, stop, duration)
	#			returns all pickups between dates or days back for duration.
	#		all columns from Locations table in db are accessable from self or as attributes of Location()

	
	print ro.address, ro.charity, ro.last_pickup

	
	for cc in ro.pickup_lines('02/01/2015', '04/03/2015'):
		print cc
		print ""
