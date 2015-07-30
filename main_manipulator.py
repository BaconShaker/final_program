#!/envs/CRES/bin/python

import os
import mysql.connector
from datetime import *
import numpy
import math
from __init__ import __sql__

from gmapper import *
import calendar
from tabulate import tabulate

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

today = datetime.now()
this_month = calendar.month_name[today.month]
last_month = calendar.month_name[today.month - 1]
# List of default things to list in list_by_location()


class Data_Manager():
	location_names = get_location_names()

	def __init__(self):
		print "You have created a Data_Manager instance in", __name__

	def list_by_location(self, location):
		# Make a summary sheet for location using information as detail specifier.
		
		smry = """SELECT MONTHNAME(`Pickup Date`) as "Month",
		ROUND(SUM(`Collectable Material`), 0), 
		ROUND(SUM(`Gallons Collected`), 0), 
		ROUND(SUM(`Expected Donation`), 2) 
			from Pickups where `Location` = "%s" 
			group by Monthname(`Pickup Date`)
			order by DATE(`Pickup Date`) DESC
			""" % (location)
		print smry
		cursor.execute(smry)
		return cursor.fetchall()




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

		
	def average_donations(self):
		print "\n\nThis is average_donations()\n"
		cursor = db.cursor()
		ssql = "SELECT `Location`, AVG(`Expected Donation`) FROM Pickups GROUP BY `Location`"
		cursor.execute(ssql)
		result = cursor.fetchall()
		result_dict = {str(key):round(val, 2) for key, val in result}

		print result_dict

		# Got the averages for each locations donations,
		# now to UPDATE the column

		for item in result_dict:
			cmd = 'UPDATE `Locations` SET `Average Donation`= %6.2f WHERE `Name` = "%s" ' %( result_dict[item] , item)
			print cmd
			cursor.execute(cmd)
			db.commit()

		print "\nDonations averaged and sql UPDATED.\n"




	def set_last_pickup(self, chk = 1):
		print "\nlast_pickup()..."
		print "Passing lastpickup(0) will result in no UPDATE; DEFAULT will UPDATE"
		cursor = db.cursor()
		launch = """SELECT 
						`Location`,
						MAX(`Pickup Date`) AS "Last Collection",
						`Arrival`,
						`Departure`,
						`Quality`,
						`Expected Income`,
						`Expected Donation`
					FROM Pickups 
					GROUP BY `Location`"""

		cursor.execute(launch)
		recent_pickups = cursor.fetchall()
		# for t in recent_pickups:
		# 	print t
		self.picker = recent_pickups

		if chk == 1:
			for pickup in recent_pickups:
				print pickup
				admin = """UPDATE Locations SET `Last Pickup`= '%s' WHERE `Name` = "%s" """ % ( pickup[1] , pickup[0] )
				print admin, '\n'
				cursor.execute(admin)
				db.commit()
		else:
			return recent_pickups


	def sum_donations_by_month(self, month = last_month):


		# self.names()
		doncursor = db.cursor()
		print "\n\nThis is sum_donations_by_month(). "
		print "Restaurants that are going to make donations in:", month, "\n"
		
		monthsql = "select `Location`, SUM(`Collectable Material`) , SUM(`Gallons Collected`),  SUM(`Expected Donation`), SUM(`Expected Income`) , `charity` from Pickups where MONTHNAME(`Pickup Date`) = '%s' group by `Location`" % (month)

		doncursor.execute(monthsql)
		grabber = doncursor.fetchall()
		# print grabber
		# monthly_donations = { key:(int(lbs), int(gallons), round(float(tot_donation),2) , charity) for key, lbs, gallons, tot_donation, cres_income, charity in  grabber }
		# print "\n\nMonthly donations: " , monthly_donations
		for rest in grabber:
			print "	", rest[0] 
		print ""	
		# display_this = [[key, (int(lbs), int(gallons), round(float(tot_donation),2) , charity)] for key, lbs, gallons, tot_donation, charity in  grabber ]
		print tabulate(grabber, headers = ["Location", "LBS", "Gallons", "Donation for " + month, "CRES Income",  "Charity"] )
		
		print "\nThe table should expand if you make the window larger. "


		return grabber

	def charity_checks_by_month(self, month = last_month):
		# Return the sum of donations to each charity. 

		looker = 'SELECT `Charity`, '
		
		
		













if __name__ == '__main__':
	writer = Data_Manager()
	# writer.list_names()
	# r = writer.charity_lookup("Vinyl")
	# print r
	# donations = writer.sum_donations_by_month("July")
	summary = writer.list_by_location("Bellweather")
	print summary
		
		