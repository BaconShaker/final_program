#!/usr/bin/python
# Send an HTML email with an embedded image and a plain text message for
# email clients that don't want to display the HTML.

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import subprocess
from tabulate import tabulate

import time
import os

def log_me(inme):
	opener = open(os.path.expanduser('~/GoogleDrive/all_in_one/log.txt'), 'a')
	opener.write(str(inme))
	opener.close()


class Mailer():
	"""docstring for Mailer
	Mailer is set to default NOT send the email as a check. 
	To send the email and the copy pass Mailer("send")."""


	def __init__(self, month, send = "no"):
		self.send = send
		self.month = month

	def list_to_html(self, summary_query):
		summary_html = ""

		# Manually parse the list from sql into html
		for detail in summary_query:
			summary_html +=  '<tr><th scope="row">' + detail[0] + '</th>'
			for num in detail[1:]:
				summary_html +=  '<td style="text-align: center">' + str(int(num)) +'</td>'
				
			summary_html += '</tr>'

		return summary_html




	def send_reciept(self, donation, contact_email, contact_name, summary_q):
		# print "You need to run list_to_html first!"
		print "This is the receipt build for %s." % ( donation[0] )
		lbs = str(int(donation[1]))
		gals = str(int(donation[2]))
		don = str(round(donation[3] , 2 ))
		
		finder = "find ~/G* -iname %s.html" % (self.month)
		
		monthly_file_path = subprocess.check_output([finder], shell = True)
		monthly_file_path = monthly_file_path[:-1]
		print "\nLooking for:", monthly_file_path
		htmly = open(monthly_file_path, 'r')
		html = str(htmly.read()) 

		html = html.replace("<!--SUMMARYROWS-->", self.list_to_html(summary_q))
		
		html = html.replace("MONTH" , self.month)
		html = html.replace("LLLBBBSSS" , lbs)
		html = html.replace("GGGAAALLL" , gals)
		html = html.replace("DDDOOONNN" , don)
		html = html.replace("CCHHHAAARRIITTTY" , str(donation[5]))
		# print html
		htmly.close()
		
		# Define these once; use them twice!
		adline = "CRES Greasecycling"
		strFrom = adline + '<renewablechicago@gmail.com>'
		strTo = contact_name + '<' + contact_email + '>'
		# robby = "Robby" + "< rshintani@gmail.com>"

		# Create the root message and fill in the from, to, and subject headers
		msgRoot = MIMEMultipart('related')
		msgRoot['Subject'] = "Grease Collection Summary"
		msgRoot['From'] = strFrom
		msgRoot['To'] = strTo
		msgRoot.preamble = 'This is a multi-part message in MIME format.'

		# Encapsulate the plain and HTML versions of the message body in an
		# 'alternative' part, so message agents can decide which they want to display.
		msgAlternative = MIMEMultipart('alternative')
		msgRoot.attach(msgAlternative)

		msgText = MIMEText('If you see this message please let us know and we will\
			resend in another format. \n	Thank you!')
		msgAlternative.attach(msgText)

		msgText = MIMEText(html, 'html')
		msgAlternative.attach(msgText)
		
		# print "msgText:\n", msgText

		# This example assumes the image is in the current directory
		logo_path = "find ~/G* -iname receipt_logo.jpg"
		logo_path = subprocess.check_output([logo_path], shell = True)[:-1]
		fp = open(logo_path, 'rb')
		msgImage = MIMEImage(fp.read())
		fp.close()

		# Define the image's ID as referenced in the html file
		msgImage.add_header('Content-ID', '<image1>')
		msgRoot.attach(msgImage)

		# Send the email (this example assumes SMTP authentication is required)
		
		smtp = smtplib.SMTP()
		smtp.connect('smtp.gmail.com:587')
		smtp.starttls()
		smtp.login('renewablechicago@gmail.com','WhitneyYoung')
		
		if self.send == "yes":
			smtp.sendmail(strFrom, strTo, msgRoot.as_string())
			# Also send a receipt copy to CRES email
			smtp.sendmail(strFrom, strFrom, msgRoot.as_string())
		else:
			os.system('clear')
			# print "\n\nYou did NOT send any emails."
			
			
		
		smtp.quit()
		# print "\n\nHere is the email that was just sent:"
		# print msgRoot.as_string()[0:1000]

		# print msgRoot.as_string()
		for_display = [donation[0], lbs, gals, don ,contact_email, contact_name]
		this_month_display = tabulate([for_display], headers = ["Location", "LBS", "GALS", "Email", "Name"])
		
		summary_display = tabulate ([x for x in summary_q])
		print "\nThis month's breakdown for:", donation[0] 
		print this_month_display
		print "\nSummary: "
		print summary_display
		
		return for_display

if __name__ == '__main__':
	print "Hold on tight!" 

	mailer = Mailer()
	
		

	