#!/Users/AsianCheddar/GoogleDrive/all_in_one/bin/python
import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import os
from oauth2client import client
from oauth2client import tools
import oauth2client
from apiclient.discovery import build
from httplib2 import Http
from cal_prompter import cal_prompt 
from cal_prompter import Calendar
from gmapper import *
from the_collector import *
import urllib
import urllib2
from bs4 import BeautifulSoup 
from __init__ import __ICNC__


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    scopes = 	['https://spreadsheets.google.com/feeds',
    			'https://www.googleapis.com/auth/calendar']

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '/GoogleDrive/all_in_one/google_creds')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets_credentials.json')

    APPLICATION_NAME = "route_handler"
    CLIENT_SECRET_FILE = os.path.expanduser('~/client_secret.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scopes)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path

    return credentials



class Route_Manager(object):
	"""docstring for Route_Manager"""


	def __init__(self, data):
		print "\n*************"
		print "You have created a Route() instance."
		self.data = data
		self.link_ams = 'http://www.ams.usda.gov/mnreports/nw_ls442.txt'
		self.link_diesel = 'http://www.eia.gov/dnav/pet/pet_pri_gnd_dcus_r20_w.htm'



	def ams_lookup(self):
		response = urllib2.urlopen(self.link_ams)
		soup = BeautifulSoup(response)
		# Ruh-roh the ams gives us a .txt file to parse
		text = soup.get_text()
		# Start at the index where Choice white appears, go to EDIBLE LARD 
		self.yg_price_text = text[text.index('Choice white') :text.index('EDBLE LARD')]
		# Do the same thing for the report location
		ams_edit = text[text.index('Des') : text.index('2015') + 4 ].replace("     ", "\n Current as of ")
		self.ams_location = ams_edit
		print "yg price:", self.yg_price_text
		print "ams_location", self.ams_location

		self.yg_price = float(raw_input("\n 	What is the price of YG you want to use for this batch of Collections?	"))

	def	diesel_lookup(self):
		print "\nStart of price_of_diesel()\n"
		diesel= urllib2.urlopen(self.link_diesel)
		dsoup = BeautifulSoup(diesel)
		# links = soup.find_all( "Current2")
		# print "This is the price of Fuel today according to: ", self.link_diesel
		dsoup.prettify()
		data = dsoup.find_all('td' , 'Current2')
		length = len(data)
		# print data[13]
		temp = str(data[13])
		price = temp[32:36]
		diesel.close()
		print "End of price_of_diesel()\n"
		self.price_of_diesel = price
		return price


	def run_route(self):

		self.ams_lookup()
		date_picker = cal_prompt()

		# filtered is a list of collections  in the order they are entered
		# 	in the google form via cell phone. 

		filtered = self.get_route_from_gform(date_picker) # LIST of DICTS
		total_distance = self.route_length(filtered) # INT
		number_of_stops = len(filtered) # INT

		collections = []

		for stop in filtered:
			# Need to add some things to the input dict before
			#	passing it through Collections. 
			stop['Total Distance'] = total_distance
			stop['Number of Stops'] = number_of_stops
			stop['Oil Price'] = self.yg_price
			stop['Service Fee'] = 0.15
			stop['Diesel Price'] = self.diesel_lookup()

			Collection(stop)

			collections += [stop]

		# collections = [Collection(stop) for stop in filtered]

		for c in collections:
			print c




		
		

	def get_route_from_gform(self, date_picker):
		# Get Auth2 credentials
		credentials = get_credentials() 
		gc = gspread.authorize(credentials)

		# open the Collection Details worksheet
		wks = gc.open("Collection Details (Responses)")
		
		# get the form responses in Dictionary form
		gform_responses = wks.worksheet("Form Responses 1").get_all_records()


		# for response in gform_responses:
		# 	print response


		# Try to make it so you can see all the pickups. 
		#	May be easier to do SQL queries. 
		# if date_picker == 'all':


		# print "Date:", date_picker

		gform_responses_by_date = []


		for row_dict in gform_responses:
			# print row_dict
			if row_dict["Pickup Date"] == date_picker:
				
				# print "	" , row_dict
				gform_responses_by_date += [row_dict]

		# print"\n These will be added:" 
		# print "	" , gform_responses_by_date 

		return gform_responses_by_date
		

	def route_length(self, routelist):
		# Take the list of routes on a pickup and return
		# 	a list with all the pertinant info to pass to collections
		# 	and make receipts.
		
		route = []
		starts = []
		stops = []
		for stopdict in routelist:
			route_info = self.data.get_location_details( stopdict["Location"] )
			route += [ str(route_info[0]) + " " + str(route_info[1]) + " " + str(route_info[2]) ]

		
		# Make two lists with starts and stops to zip together
		#	pass the result to googlemaps. 
		starts += route
		starts.insert(0, (__ICNC__) )
		stops += route 
		stops.append((__ICNC__))
		legs = zip(starts, stops)

		total_dist = GoogleMap(legs).google_directions()


		return total_dist

	



if __name__ == '__main__':
	from main_manipulator import *
	r = Data_Manager()
	test = Route_Manager(r)
	test.get_route_from_gform()
	
		