#!/envs/CRES/bin/python

# This is the Storage and oil on hand(ler) class


import os
import mysql.connector
from __init__ import  __robby__

import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
import os
from oauth2client import client
from oauth2client import tools
import oauth2client
from apiclient.discovery import build
from httplib2 import Http

# Establish connection to SQL server.
db = mysql.connector.connect(**__robby__)
cursor = db.cursor()


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
    
    
    
    

def sum_gallons():
	cursor.execute(
		"""
		SELECT 
			SUM(`Gallons Collected`)
		FROM
			`Pickups`
			
		"""
	)
	
	try:
		return int( cursor.fetchall()[0][4] )
	except IndexError:
		print "There was a problem looking up the Expected Gallons"
		
		
		
		
 
class Inventory():
	# Establish some properties:
	
	on_hand = sum_gallons()
	
	def __init__(self):
		print "This is an instance of Inventory, the inventory class."
		print "	We should have ~", self.on_hand, "gallons at the ICNC currently."
		
		
		
	def fill_levels(self):
		# Get Auth2 credentials
		credentials = get_credentials() 
		gc = gspread.authorize(credentials)

		# open the Collection Details worksheet
		wks = gc.open("Fill Level (Responses)")
		
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
			print row_dict
			#~ if row_dict["Pickup Date"] == date_picker:
				
				#~ # print "	" , row_dict
				#~ gform_responses_by_date += [row_dict]

		#~ # print"\n These will be added:" 
		#~ # print "	" , gform_responses_by_date 

		#~ return gform_responses_by_date
		
	
	
	
	
	
	
if __name__ =="__main__":
	icnc = Inventory()
	print icnc.fill_levels()
	
