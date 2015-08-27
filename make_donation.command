#!/envs/CRES/bin/python

# This is the main Script for making donations. 


from p_files.main_manipulator import *
from p_files.e_mailer import *


def main():
	print "\n\nThis is the main Script for making donations. "
	print "Which month would you like to look at?"
	month = raw_input("	BLANK = " + last_month + " or type the monthname here... ")
	if month == "":
		month = last_month

	master = Data_Manager()
	donations = master.sum_donations_by_month(month) #returns {location (details tuple)}


	ask = raw_input("\n\nType 'yes' to send receipts. Anything else will be rejected. ")
	email = Mailer(month, send = ask)
	for donation in donations:
		loc_name = donation[0]
		print "Location:", loc_name


		contact = master.get_location_details( loc_name )
		summary = master.list_by_location(loc_name)
		num_charities = len(master.charities)
		agg_donation = master.aggregate_donations()

		log_me( email.send_reciept(donation, contact,  summary , num_charities, agg_donation), contact[10] )










if __name__ == '__main__':
	main()
