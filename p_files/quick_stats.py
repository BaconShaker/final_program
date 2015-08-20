#!/envs/CRES/bin/python

import ttk
from Tkinter import *
from sql_ops import *
check_sql = CRES_SQL()
check_sql.is_running()
from main_manipulator import *
from tabulate import tabulate


# start the page
page = Tk()
# give it a name
page.title("Quick Stats")
# setup the main window frame
mainframe = ttk.Frame(page, padding = " 3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# start up the database
database = Data_Manager()
print ""
names =  database.location_names
print ""
print database.charities
for name in names:
	pickups = database.list_by_location(name)
	print ""
	print name + ":"
	
	print tabulate(pickups, headers = ["Month", "LBS Collected", "Gallons", "Donation" ])
