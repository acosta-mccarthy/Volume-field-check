#!/usr/bin/env python3

"""Email me list of items with volume fields created yesterday

Author: Nina Acosta
"""

import psycopg2
import xlsxwriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
from datetime import date, timedelta
yesterday = date.today() - timedelta(1)
subject = yesterday.strftime ("%m/%d/%Y") #Format date for Subject line

# SQL Query:
q='''SELECT
CONCAT('i',item_view.record_num, 'a', '          ', field_content)
--adds i prefix to the item record number and the "a" as a placeholder for the check digit, so the number can be easily copied and pasted into Sierra, also includes the text of the volume field

FROM sierra_view.varfield_view
JOIN sierra_view.item_view ON varfield_view.record_num = item_view.record_num

WHERE
record_creation_date_gmt > TIMESTAMP 'yesterday' AND
varfield_view.record_type_code =  'i' AND
varfield_type_code = 'v'
-- This limits results to any item records created since midnight of the previous day, that contain something in the volume field

ORDER BY field_content
--sorts results alphabetically by the text included in the volume field
'''
#This code uses placeholder info to connect to Sierra SQL server, please replace with your own info
conn = psycopg2.connect("dbname='iii' user='******' host='000.000.000.000' port='1032' password='******' sslmode='require'")

#Open session and run query
cursor = conn.cursor()
cursor.execute(q)
rows = cursor.fetchall()
conn.close()

convert = str(rows)
data = convert.replace("',), ('", "\r\n").replace("[('", "").replace("',)]","") #Create linebreaks between results in email

# These are variables for the email that will be sent.
# This code uses placeholders, please add your own email server info
emailhost = 'email.server.midhudson.org'
emailuser = 'emailaddress@midhudson.org'
emailpass = '*******'
emailport = '587'
emailsubject = 'Volume fields created ' + str(subject)
emailmessage = '''

The items listed below were created yesterday and included a volume field.
Please review for possible errors.

''' +str(data) #Appends SQL results to the end of the email

emailfrom= 'emailaddress@midhudson.org'
emailto = 'nacosta@midhudson.org'


#Create an email with an attachement
msg = MIMEMultipart()
msg['From'] = emailfrom
if type(emailto) is list:
    msg['To'] = ', '.join(emailto)
else:
    msg['To'] = emailto
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = emailsubject
msg.attach (MIMEText(emailmessage))
#msg = MIMEText(type._htmlBody, "html")
#Send the email
smtp = smtplib.SMTP(emailhost, emailport)
#for Google connection
smtp.ehlo()
smtp.starttls()
smtp.login(emailuser, emailpass)
#end for Google connection
smtp.sendmail(emailfrom, emailto, msg.as_string())
smtp.quit()
