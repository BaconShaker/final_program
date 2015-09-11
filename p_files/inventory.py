#!/envs/CRES/bin/python

# This is the Storage and oil on hand(ler) class


import os
import mysql.connector
from __init__ import __sql__

# Establish connection to SQL server.
db = mysql.connector.connect(**__sql__)
cursor = db.cursor()

def sum_gallons():
	cursor.execute(
		"""
		SELECT 
			SUM(`Gallons Collected`)
		FROM
			`Pickups`
			
		"""
	)
	return int( cursor.fetchall()[0][0] )
 
class Inventory():
	# Establish some properties:
	
	on_hand = sum_gallons()
	
	def __init__(self):
		print "This is an instance of Inventory, the inventory class."
		print "	We should have ~", self.on_hand, "gallons at the ICNC currently."
		
	
	
	
	
	
	
if __name__ =="__main__":
	icnc = Inventory()
	
