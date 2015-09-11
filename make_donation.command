#!/envs/CRES/bin/python

# This is the main Script for making donations. 


from p_files.main_manipulator import *
from p_files.e_mailer import *


def main():
	print "\n\nThis is the main Script for making donations. "
	print "\n	Use me like this: *** %s month [send = yes/no]" % (sys.argv[0]) + " *** for full control."
	print "\n	Use me like this: *** %s month" % (sys.argv[0]) + " *** for just a printout."
	print "\n"
	
	if len(sys.argv) == 3:
		month = sys.argv[1]
		ask = sys.argv[2]
		
	elif len(sys.argv) == 2:
		print "I can only check one argument at a time so month has been set to", last_month + '.'
		month = sys.argv[1]
		ask = 'no'
	
	else:
		month = raw_input("	BLANK = " + last_month + " or type the monthname here... ")
		ask = raw_input("\n\nType 'yes' to send receipts. Anything else will be rejected. ")
		
	if month == "":
		month = last_month

	master = Data_Manager()
	donations = master.sum_donations_by_month(month) #returns {location (details tuple)}

	
	email = Mailer(month, send = ask)
	for donation in donations:
		loc_name = donation[0]
		#~ os.system('clear')
		print "\n\n\n\n\n	Location:", loc_name


		contact = master.get_location_details( loc_name )
		summary = master.list_by_location(loc_name)
		num_charities = len(master.charities)
		agg_donation = master.aggregate_donations()

		log_me( email.send_reciept(donation, contact,  summary , num_charities, agg_donation), contact[10], month )

		
		
	if ask != 'yes':
		os.system('clear')
		print "\n\n		You did NOT send any emails.\n\n\n\n"
			
		








if __name__ == '__main__':
	main()
