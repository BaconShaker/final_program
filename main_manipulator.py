#!/envs/CRES/bin/python

import os
import mysql.connector
from datetime import *
import numpy
import math
from __init__ import __sql__

from gmapper import *

db = mysql.connector.connect(**__sql__)
cursor = db.cursor()


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def get_location_names():
	# This little bugger makes the master names lists for other scripts
	cursor.execute("SELECT `Name` FROM `Locations`")
	namer = [n[0] for n in cursor.fetchall()]
	print "\nNames: "
	# for name in namer:
	# 	print "	",name
	return namer

class Data_Manager():
	location_names = get_location_names()

	def __init__(self):
		print "You have created a Data_Manager instance in", __name__



	def average_collections_by_location(self):
		# Resets the average collection col to include any new collecitons. 
		print "\nThis is averageing the collections..."
		average_sql = """SELECT `Location`, round(AVG(`Gallons Collected`) , 2) as "Average Collection" from Pickups group by `Location`"""
		cursor.execute(average_sql)
		collection_averages = cursor.fetchall()
		for thing in collection_averages:
			mean_sql = """UPDATE Locations SET `Average Collection`= %s WHERE `Name` = "%s" """ % (thing[1], thing[0])
			cursor.execute(mean_sql)
			db.commit()



	def get_location_details(self, place_to_lookup):
		# Grab the Address, city zip and email... for the route maker
		squeeky = 'SELECT `Address`, `City`, `Zip`, `Email`, `Phone Number`, `Contact`, `Last Pickup`, `Charity`, `Total Donation`, `Notes`, `Name` FROM `Locations` WHERE `Name` LIKE \"%' + place_to_lookup[0:7] + '%\"'
		cursor.execute(squeeky)
		route_info = cursor.fetchall()
		# print "Route info for", place_to_lookup, ": ", route_info[0], "\n"
		return route_info[0]

	def list_names(self):
		print self.location_names

	def add_dict_to_db(self, tablename, rowdict):
		# This function adds a dictionary row to the specified table 
		# in the CRES database
		print "This function will add the dictionary provided to the table specified."
		print 'add_dict_to_db( tablename, rowdict )'
		print 'tablename: ', tablename
		print 'rowdict: ', rowdict

		# filter out keys that are not column names
		# you have to add new columns in the sqladmin page
		cursor.execute("describe %s" % tablename)
		allowed_keys = set(row[0] for row in cursor.fetchall())
		keys = allowed_keys.intersection(rowdict)

		if len(rowdict) > len(keys):
			unknown_keys = set(rowdict) - allowed_keys
			# print "\n\nskipping keys:", ", ".join(unknown_keys)

		columns = "`" + "`,`".join(keys) + "`"

		values_template = ", ".join(["%s"] * len(keys))
		values = tuple(rowdict[key] for key in keys)

		sql = 'insert into %s (%s) values %s' % (
			tablename, columns, values)

		os.system('clear')

		# print "\n\n This is the SQL query: ", sql

		# As of 7/21 this part will add any collections in a list of collections
		# to the database. I want to change that so it either doesn't add any unless the whole list 
		# is ok, or make it so it checks for similar entries and updates rather than cancel out. 
		#	There's more in route_handler.add_collections_to_db()
		
		cursor.execute(sql)
		db.commit()
		
		print "\n\n\nJolly good mate! I added the collections to the database, you're all good to go! "



	def charity_lookup(self, location):
		query = 'SELECT `Charity` FROM Locations WHERE `Name` = "%s"' % (location)
		cursor.execute(query)
		charity_name = cursor.fetchall()
		return str(charity_name[0][0])


	# def build_route(self, routelist):
	# 	print "This is build route"
	# 	print "the route is ", self.route_length(routelist) , "miles long."

		











		
		













if __name__ == '__main__':
	writer = Data_Manager()
	# writer.list_names()
	r = writer.charity_lookup("Vinyl")
	print r
		
		