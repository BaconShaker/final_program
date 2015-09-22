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
from inventory import get_credentials
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import os
from oauth2client import client
from oauth2client import tools
import oauth2client
from apiclient.discovery import build
from httplib2 import Http

# Set today, this month and last month variables.
today = datetime.now()
this_month = calendar.month_name[today.month]
last_month = calendar.month_name[today.month - 1]

# Establish connection to SQL server.
db = mysql.connector.connect(**__sql__)
cursor = db.cursor()


# Some generic functions
def charities_dict(texty = False):

	cursor.execute("SELECT Name, Supporters from Charities")
	ch = {x[0] : x[1].split(", ") for x in cursor.fetchall()}
	if texty:
		print '\nCharities list: '
		for c in ch:
			print "	", c, ":", ch[c]
	return ch

def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

def estimate_sale_date(gals, days, target = 6000):
	gpd = gals / days
	to_go = target - gals
	days_till = int(to_go / gpd)
	today = datetime.today().date() 
	estimated_sale_date = today + timedelta(days = days_till)
	return estimated_sale_date

	

def get_location_names(texty = False):
	# This little bugger makes the master names lists for other scripts
	cursor.execute("SELECT `Name` FROM `Locations`")
	namer = [n[0] for n in cursor.fetchall()]
	if texty:
		print "\nLocations: "
		for name in namer:
			print "	",name
	return namer




# The main event!
class Data_Manager():
	location_names = get_location_names()
	charities = charities_dict()

	def __init__(self):
		print "\n\n I have created a Data_Manager instance in", __name__

	# Adds a dict or list of dicts to a table. 
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




	def get_new_clients(self):
		# Get Auth2 credentials
		credentials = get_credentials() 
		gc = gspread.authorize(credentials)

		# open the Collection Details worksheet
		wks = gc.open("Collection Details (Responses)")
		
		# get the form responses in Dictionary form
		gform_responses = wks.worksheet("Form Responses 1").get_all_records()
		new_clients = []

		for row_dict in gform_responses:
			# print row_dict
			if row_dict["Add_type"] == "Add Client" and row_dict["Name"] not in self.location_names:
				
				# print "	" , row_dict
				new_clients += [row_dict]

		# print"\n These will be added:" 
		# print "	" , gform_responses_by_date
		

		self.new_clients = new_clients


	def add_new_clients(self):
		self.get_new_clients()
		if len(self.new_clients) > 0:
			
			for new_loc_dict in self.new_clients:
				
				if len(new_loc_dict['Client Notes']) == 0:
					new_loc_dict['Client Notes'] = "Nothing to report"

					
				try:
					new_loc_dict['Zip'] = int(new_loc_dict['Zip'])
					
					

				except ValueError as error:
					print "\n	 There seems to be a problem with the zip code from the GoogleSheet."
					new_loc_dict['Zip'] = 111

				try:
					new_loc_dict['Dumpster'] = int(new_loc_dict['Dumpster'] )
				except ValueError :
					new_loc_dict['Dumpster'] = 000

				try:
					new_loc_dict['Quality'] = int(new_loc_dict['Quality'] )
				except ValueError :
					new_loc_dict['Quality'] = 0
					
					
				self.add_dict_to_db("Locations", new_loc_dict)
				print "I added", new_loc_dict, "to the database."
		else:
			print "There are no new clients to add nothing to add" 
		






		

	# Return the sum of all donations made since the Dawn of CRES
	def aggregate_donations(self):
		cursor.execute(
			"""	SELECT
					ROUND(SUM(`Expected Donation`))
					From Pickups
					Where 1
			""")
		ag_don = cursor.fetchall()
		return ag_don[0][0]

	# Updates CRES.Locations `Average Gallons` collected
	def average_collections_by_location(self):
		# Resets the average collection col to include any new collecitons. 
		print "\nThis is averageing the collections..."
		average_sql = """SELECT 
							`Location`, 
							round(AVG(`Gallons Collected`) , 2),
							round(SUM(`Gallons Collected`))
							from Pickups 
							group by `Location`"""
		cursor.execute(average_sql)
		collection_averages = cursor.fetchall()
		for thing in collection_averages:
			mean_sql = """UPDATE Locations 
							SET `Average Collection`= %s , 
								`Total Gallons` = %s 
							WHERE `Name` = "%s" """ % (thing[1], thing[2], thing[0])
			cursor.execute(mean_sql)
			db.commit()

	# Updates CRES.Locations `Average Donations` 		
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

	# Returns Charity string for Location	
	def charity_lookup(self, location):
		# Should put a try/except here for when you have a name in the gform that doesn't match the MAMP
		query = 'SELECT `Charity` FROM Locations WHERE `Name` = "%s"' % (location)
		cursor.execute(query)
		charity_name = cursor.fetchall()
		print "This is looking up the charity for:", location
		return str(charity_name[0][0])

	# 	*** NOT DONE ***
	# 	Return the value for each Charity check for the previous month.
	def charity_checks_by_month(self, month = last_month):
		# Return the sum of donations to each charity. 

		looker = """SELECT  
			Charity, 
			COUNT(Location) AS "Collections",
			ROUND( SUM(`Expected Donation`),2) AS "Aggregate Donation"
		from `Pickups` 
		WHERE Charity in 
			(SELECT Name from Charities)
			AND
				MONTHNAME(`Pickup Date`) = "%s" 
		GROUP BY Charity""" % (month)
		cursor.execute(looker)
		to_return = cursor.fetchall()

		# Print out a pretty table for funzies.
		print tabulate(to_return, headers = ["Charity", "# Collections", "Donation for " + month])
		return to_return


	# Calculates `Next Pickup1 date:
	#	1. By averaging the day between ACTUAL collctions and
	#	2. Calculates average gallons/day and plots a date
	#
	#	Does NOT return anything
	def collection_analysis(self): # Needs comments!
		# Finds the average number of days between pickups 
		print "\n\nThis is collection_analysis()"
		cursor = db.cursor()
		
		day_dict = {}
		gal_dict = {}

		for ent in self.location_names:

			finder = """SELECT 
							`Pickup Date`,
							`Gallons Collected`,
							`Arrival`,
							`Departure`,
							`Quality`,
							`Expected Income`,
							`Expected Donation`
						FROM Pickups 
						WHERE `Location` = "%s" """ % (ent)
			cursor.execute(finder)
			sparks = cursor.fetchall()
			print ent
			cou = 0
			day_list = []
			gal_list = []

			# Sparks is a list of pickups from each Location
			for spark in sparks:
				# print cou, spark
				cou += 1
				
				if cou <= len(sparks) - 1:
					
					days_btw_pickups = days_between(str(sparks[cou][0]), str(spark[0]))
					day_list.append(days_btw_pickups)

					gal_list.append(sparks[cou][1])

				else:
					# Runs when the iterator gets to the end of the pickups/restaurant
					# 	It's because you want the days between..

					ziplist = zip(day_list, gal_list)
					# print ziplist
					gal_per_day = []
					for z in ziplist:
						gal_per_day.append(z[1]/z[0])

					# Predict next pickup by actual gallons collectd.
					gal_per_day =round(numpy.mean(gal_per_day), 0)
					print "	Gallons per day:", gal_per_day
					fill_time_by_gallons = round(200/gal_per_day , 0)
					

					print "	Fill Time by gallons collected: " , fill_time_by_gallons  , "days"
					
					# "Fill time" by actual pickups--more like actual pickup average
					average_fill_time = round(numpy.mean(day_list), 0)
					
					if not math.isnan(average_fill_time):
						fill_time_by_gallons = int(fill_time_by_gallons)
						print "	Average time between pickups: ", int(average_fill_time), "days."
						print "	Fill Time by gallons collected: " , fill_time_by_gallons  , "days."
						day_dict[ent] = average_fill_time
						gal_dict[ent] = fill_time_by_gallons

			print "" #Still iterating through location_names here
		# print "Day_dict: ", day_dict
		
		# print "Gal_dict: ", gal_dict

		# Making sure last pickup is up to date.
		self.set_last_pickup()

		for key in day_dict:
			# print key, day_dict[key], gal_dict[key]
			planner = 'UPDATE Locations SET `Fill Time` = %s, `Fill Time Gallons` = %s WHERE `Name` = "%s"' % ( day_dict[key] , gal_dict[key], key )
			cursor.execute(planner)
			db.commit()

			# print planner 

			looklast = 'SELECT `Name`, `Last Pickup` from Locations where `Name` = "%s" ' % (key)
			cursor.execute(looklast)
			looklast = cursor.fetchall()
			nextpick = {key: las[1]+ timedelta(day_dict[key]) for las in looklast}
			nextpick_gal = {key: las[1]+ timedelta(gal_dict[key]) for las in looklast}
			# print "nextpick: " , nextpick
			# print "nextpick_gal: " , nextpick_gal

			next = """UPDATE Locations SET `Next Pickup` = "%s", `Next Pickup Gallons` = "%s" where `Name` = "%s" """ % (nextpick[key], nextpick_gal[key] ,key )
			# print next
			cursor.execute(next)
			db.commit()

		print "\n"*5 
		for r in day_dict:
			print "We go to", r , "every", day_dict[r], "but it should take ~", gal_dict[r] ,"days to fill.\n"
		# return day_dict

	# Figure sale date and update analysis table
	def figure_next_sale(self):
		needed = 6000 
		cursor.execute(
			"""SELECT
					round(sum(`Gallons Collected`)) as "Actual Collected Gallons",
					round(sum(`Gallons Collected`) * avg(Quality)/100)  as "Gallons x Quality",
					datediff( max(`Pickup Date`), min(`Pickup Date`)) as "Days" 
				from 
					Pickups
							""")

		stats = cursor.fetchall()[0]
		stats = {
			'current' : stats[0],
			"quality" : stats[1],
			"day_count" : stats[2]
			}
		
		actual = estimate_sale_date(stats['current'], stats['day_count'])
		with_quality = estimate_sale_date(stats['quality'], stats['day_count'])
		# print "Date by actual gallons:", actual
		# print "Date by quality gallns:", with_quality

		cursor.execute(
			"""UPDATE 
				Analysis
				set 
					On_hand = %s,
					Quality = %s,
					`Next_sale(Q)` = '%s',
					`Next_sale(A)` = '%s'
				where 
					1
					
				""" % (stats['current'], stats['quality'], with_quality, actual)
			)
		db.commit()
		return stats







	# Makes a list of Supporters for CRES.Charities for each Location. 
	# Only writes to db if there are changes to be made. 
	# Does NOT return anything, at most it will db.commit().
	def fix_supporters(self):
		print "Updating supporters?"
		from sets import Set
		made_changes = 0

		# Need a list of Charities

		charities = self.charities

		# Then for each name on the list get a list of charity names
		for charit in charities:
			
			# Check if an update is needed... This is what we have 'now'
			current = charities[charit]
			
			# This is what we 'want'
			cursor.execute('SELECT Name from Locations where Charity = "%s"' % (charit))
			new = [x[0] for x in cursor.fetchall()]
			
			# print current
			final = Set(new).difference(current)
			length = len(final)
			i = 1
			done = ""
			for x in final:
				if i < length:
					done += x + ", "
					i += 1
				else:
					done += x
			print done
			if len(final) != 0:
				print "	Yes\n\n 	Supporters list has been updated successfully for:", charit
				print "		CURRENT: ", current
				print "		NEW:", new
				print "		Final:", final, len(final)
				# for new_sup in final:
				cursor.execute('UPDATE Charities SET Supporters = "%s" WHERE Name = "%s"' % (done, charit))
				db.commit()
				made_changes = 1

		if made_changes != 1:
			print "\n*****************"
			print "It's not me, it's you. You didn't add/make any changes to Charity Supporters, so let us move on."
			print "*****************"
		else:
			print "Mischief Managed... Supporters are all up to date."



			

	# Establish route_info and return.
	def get_location_details(self, place_to_lookup):
		# Grab the Address, city zip and email... for the route maker
		#~ print place_to_lookup
		squeeky = 'SELECT `Address`, `City`, `Zip`,`Email`, `Phone Number`, `Contact`, `Last Pickup`, `Charity`, ROUND(`Total Donation`), `Notes`, `Name`, `Total Gallons` FROM `Locations` WHERE `Name` LIKE \"%' + place_to_lookup[0:7] + '%\"'
		cursor.execute(squeeky)
		route_info = cursor.fetchall()
		# print "Route info for", place_to_lookup, ": ", route_info[0], "\n"
		return route_info[0]





		

	# Returns a monthly summary for location provided
	def list_by_location(self, location):
		# Make a summary sheet for location using information as detail specifier.
		# ROUND(SUM(`Collectable Material`), 0), 
		smry = """SELECT 
					MONTHNAME(`Pickup Date`) as "Month",
					ROUND(SUM(`Gallons Collected`), 0), 
					ROUND(SUM(`Expected Donation`), 2)
				from Pickups 
				where `Location` = "%s" 
				group by Monthname(`Pickup Date`)
				order by DATE(`Pickup Date`) DESC
				""" % (location)
		# print smry
		cursor.execute(smry)
		return cursor.fetchall()

	# Return a list of pickups for month given
	def pickups_by_month(self, month = last_month):
		cursor.execute(
			"""	SELECT Location, `Gallons Collected` 
				from Pickups 
				where MONTHNAME(`Pickup Date`) = '%s'
				""" % (month)
			)
		print cursor.fetchall()






		

	# Looks for most recent pickup and UPDATES CRES.Locations
	def set_last_pickup(self, chk = 1):
		print "\nlast_pickup()..."
		print "Passing lastpickup(0) will result in no UPDATE; DEFAULT will UPDATE"
		cursor = db.cursor()
		launch = """SELECT 
						`Location`,
						MAX(`Pickup Date`) AS "Last Collection",
						SUM(`Expected Donation`),
						SUM(`Gallons Collected`)
					FROM Pickups 
					GROUP BY `Location`"""

		cursor.execute(launch)
		recent_pickups = cursor.fetchall()
		# for t in recent_pickups:
		# 	print t
		# self.picker = recent_pickups

		if chk == 1:
			print "	*****************	*****************	*****************"
			print "You are about to write changes to the database."
			print "	*****************	*****************	*****************"
			for pickup in recent_pickups:
				# print pickup
				admin = """UPDATE 
							Locations 
						SET 
							`Last Pickup`= '%s', 
							`Total Donation` = %s, 
							`Total Gallons` = %s 
						WHERE `Name` = "%s" 
						""" % ( pickup[1] , pickup[2], pickup[3], pickup[0] )
				# print admin, '\n'
				cursor.execute(admin)
				db.commit()
		else:
			print "\n 	You did not write set_last_pickup to the database."
			return recent_pickups

	
	# Returns a list of all the donations/collections made in month
	def sum_donations_by_month(self, month = last_month, texty = False):

		# self.names()
		doncursor = db.cursor()
		
		monthsql = """select 
						`Location`, 
						SUM(`Collectable Material`) , 
						SUM(`Gallons Collected`),  
						SUM(`Expected Donation`), 
						SUM(`Expected Income`) , 
						`charity` 
						from 
							Pickups 
						where 
							MONTHNAME(`Pickup Date`) = '%s' 
						group by 
							`Location`
						
						""" % (month)

		doncursor.execute(monthsql)
		grabber = doncursor.fetchall()
		
		if texty:
			print "\n\nThis is sum_donations_by_month(). "
			print "Restaurants that are going to make donations in:", month, "\n"
			for rest in grabber:
				print "	", rest[0] 
			print ""	
		
			print tabulate(grabber, headers = ["Location", "LBS", "Gallons", "Donation for " + month, "CRES Income",  "Charity"] )
		
			print "\nThe table should expand if you make the window larger. "

		return grabber


	

			
	

if __name__ == '__main__':
	writer = Data_Manager()
	# writer.list_names()
	# print writer.charity_lookup("Kappy's Diner & Pancake House")
	# print r
	# donations = writer.sum_donations_by_month("August")
	# summary = writer.list_by_location("Bellweather")
	# writer.fix_supporters()
	#~ print writer.set_last_pickup()
	print writer.add_new_clients()
	# print writer.collection_analysis()
	# print "This is donations"
	# print "	", donations

	# writer.pickups_by_month("August")
	# print "\n\nThis is summary"
	# print "	", summary
	# writer.aggregate_donations()
	#~ writer.figure_next_sale()


	# print writer. charity_checks_by_month()
