#!/Users/AsianCheddar/GoogleDrive/all_in_one/bin/python
# This is the googlemaps api version of jedi.py

from googlemaps import Client
import json
from tabulate import tabulate
from __init__ import google_api_key


# start = '2256 n kedzie blvd 60647'
# stop = '2804 w logan blvd 60647'

class GoogleMap():
	"""docstring for Leg"""
	def __init__(self, trip, *args):
		# Trip must be a list of addresses, the class will take care of the waypointing. 
		print "The useage for this little guy is simple, just pass GoogleMap( (START, STOP) )\n\
		 and you'll be good to go in no time! \n\
		 Have a nice day!"
		self.trip = trip
		print trip
		# self.starts = [ start[0] for start in trip ]
		# self.stops = [ stop[1] for stop in trip ]

		# print "\n\n"
		# print "Start: ", self.starts
		# print "Stop: " , self.stops
		
		print "________-----------_______"
		
		
	def google_directions( self ):

		# initalize a googlemaps object
		googmap = Client(google_api_key)

		print '\n\n'

		# call the .directions() funciton on Client, save in a list
		# See if we should use waypoint optimixzing?

		list_of_maps = [ googmap.directions( pitstop[0], pitstop[1] ) for pitstop in self.trip ]

		print "\n\n\n******************************\n\n\n"


		# print directions['Directions']['Distance']["meters"]
		# for thing in list_of_maps:
		# 	print "\n\n\n\n"
		# 	print thing

		total_distance = 0
		for count, gmap in enumerate(list_of_maps): 
			# Iterate through the list
			if gmap[0]['legs'][0]['distance']['text'][-2:] == "ft":
				total_distance = 0.10
			else:
				
				total_distance += round(   float(gmap[0]['legs'][0]['distance']['text'].replace( ' mi', ''))  ,  2 )
			steps =  gmap[0]['legs'][0]['steps'] 
			display = []
			turn = 0
			leg = 0
			for step in steps:
				to_go = step['distance']['text']
				# total_distance += int(to_go)
				turn = turn + 1
				words = step['html_instructions']
				words = words.replace( '<b>' , ' ')
				words = words.replace( '</b>' , ' ')
				words = words.replace( '<div style="font-size:0.9em">' , '')
				words = words.replace( '</div>' , ' ' )
				display.append([turn,  to_go, words])
			# print display

			tabs = ["Turn", "Distance", "Instruction"]

			tab = tabulate(display, headers = tabs, tablefmt = "simple")
			print "LEG # " , count , "\n"
			print tab
			final = []
			final.append(tab)
			# print tab
		# return directions
		print "\n\nDistance: ", total_distance
		print "\n\n\n******************************\nEnd of google_directions().\n\n"
		# return final
		return total_distance





#-------------------------------
# FOR DEBUGGING:
# 	inp is a replica of the input to to be expected from main_program. 

# inp = [ 
# 		('2021 W Fulton 60612', '2256 n kedzie blvd 60647'),
# 		('2256 n kedzie blvd 60647', '2804 w logan chicago 60647') ,
# 		('2804 w logan chicago 60647','2021 W Fulton 60612')


# 	]
# r = GoogleMap( inp )
# jog = r.google_directions()
# print jog
