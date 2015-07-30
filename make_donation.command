#!/envs/CRES/bin/python

# This is the main Script for making donations. 


from main_manipulator import *
from e_mailer import *


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
		print "\n"
		email.list_to_html( master.list_by_location(donation[0]) )
		log_me( email.send_reciept(donation))










if __name__ == '__main__':
	main()