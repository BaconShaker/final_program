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

	email = Mailer(month, send = "no")
	for donation in donations:
		email.send_reciept(donation)










if __name__ == '__main__':
	main()