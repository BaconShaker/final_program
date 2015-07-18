#!/Users/AsianCheddar/GoogleDrive/all_in_one/bin/python
# Just take the inputs and do conversions

from tabulate import tabulate
from datetime import *

print "Imported Collections"
# Variables we need:
# 	location
# 	height on arrivial
# 	height on departure
# 	price of oil
# 	route
# 	pickup 
# 		duration
# 		date 
# 		quality
# 		score
# 		fuel surcharge
# 			route / stops


# input should look like: 
	
# 		[ location ]

class Collection():
	"""docstring for Collection"""
	
	def __init__(self, inputs):
		# Bring in the input dictionary and store it to self for later reference
		# print "\n\n\ninputs from Collection: " , inputs
		self.route = {
						"Total Distance" : inputs["Total Distance"],
						"Number of Stops" : inputs["Number of Stops"]
						}

		# Given: 
		h = 36
		w = 28
		l = 48

		t_vol = 0.0043290 * l * w * h

		# Convert Gallons Arrivial and Departure from strings to doubles
		inputs['Height on Arrival'] = float(inputs['Height on Arrival'])
		inputs['Height on Departure'] = float(inputs['Height on Departure'])
		# inputs['Oil Price'] = float(inputs['Oil Price'])


		inputs['Gallons Arrival'] = round(0.0043290 * l * w * inputs['Height on Arrival'] , 2)
		inputs['Gallons Departure'] = round(0.0043290 * l * w * inputs['Height on Departure'] , 2)
		inputs['Gallons Collected'] = round(inputs['Gallons Arrival'] - inputs['Gallons Departure'] , 2)
		score = inputs['Gallons Collected'] / inputs['Gallons Arrival'] 
		inputs['Score'] = round(score * 100 , 2)

		# 7.75 lbs per gallon is set here
		lbs_collected = inputs['Gallons Collected'] * 7.75 

		# Original
		# inputs['Expected Revenue'] = round(inputs['Oil Price'] * lbs_collected , 2)
		print "\n******************* Back to the future ********************"
		print "lbs_collected:", lbs_collected
		print "Quality:", inputs['Quality'], "\n"

		# New
		lbs_adjusted = lbs_collected * inputs['Quality'] / int(100)
		inputs['Expected Revenue'] = round(float(inputs['Oil Price']) * float(lbs_adjusted ), 2)
		inputs['Adjusted LBS'] = lbs_adjusted


		donation = inputs['Oil Price'] - float(inputs['Service Fee']) 

		inputs['Donation Rate'] = round(donation , 2) 
		inputs['Expected Income'] = round(inputs['Service Fee'] * lbs_collected, 2)
		# inputs['Expected Donation'] = round( lbs_adjusted * donation , 2) 
		inputs['Expected Donation'] = round( inputs['Expected Revenue'] - inputs['Expected Income'] , 2) 
		inputs['Collectable Material'] = round(lbs_collected,2)
		
		# Need to account for the penalty associated with poor quality in the income that CRES will get
		# Revenue - (Income + Donation) = | Excess / Penalty |
		
		# This should dissappear
		

		self.indict = inputs

		print "\n\n 	INDICT "
		print tabulate( [( e, self.indict[e] ) for e in self.indict] , ["Key", "Value"])
		

		# Need to calculate the fuel surcharge, this is the program that
		# takes care of that. The inputs are continued below. 

		def route_analizer():

			# Takes the self.route which should be in the form:
			# 	{ 
			# 		"Total Distance" : 3,
			# 		"Number of Stops" : 3,
			# 	}
			# And returns the fuel charge for the collection being initiated.

			tdist = self.route['Total Distance']
			num_stops = self.route['Number of Stops']
			diesel_price = self.indict['Diesel Price']
			mpg_truck = 8


			fuel_surcharge = float(tdist)/ mpg_truck * float(diesel_price) / int(num_stops)
			fuel_surcharge = round(fuel_surcharge , 2)
			print "\nFuel Surcharge(): ", fuel_surcharge
			return fuel_surcharge


		f_surcharge = route_analizer()

		
		self.indict['Fuel Surcharge'] = f_surcharge

		self.indict['Miles in Route'] = self.route['Total Distance']
		self.indict['Stops in Route'] = self.route['Number of Stops']

		# Need to adjust expected income and donation amounts

		self.indict['Expected Income'] = self.indict['Expected Income'] + f_surcharge
		self.indict['Expected Donation'] = self.indict['Expected Donation'] - f_surcharge

		
		# print tabulate(  [ ( key , self.indict[key] ) for key in self.indict  ]  )

		#This is a debugging checker.
		# Make sure the total revenue = cres + donation + f_surcharge

		# print "This 0 =", self.indict['Expected Revenue'] - self.indict['Expected Income'] - self.indict['Expected Donation'] - self.indict['Fuel Surcharge']

	# Make anobject that outside programs can return and use
	def run(self):
		if len(self.indict["Pickup Date"]) == 0:
			da = datetime.now().date()
			self.indict['Pickup Date'] = str(da)
			
		print '\n\n'  , self.indict ,  "\n\n"

		print "Collection.run()"
		return self.indict

		



if __name__ == '__main__':
	txtfile = open('./price.txt' , 'rb')
	readfile = txtfile.readlines()
	# print readfile
	import re
	for line in readfile:
		line = line.rstrip()
		print line
		








