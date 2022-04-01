#!/usr/bin/env python3
import os
import smtplib 

sender_address = "XXXX@gmail.com" # Replace this with your Gmail address
receiver_address = "XXXX0@gmail.com" # Replace this with any valid email address
account_password = "XXXX" # Replace this with your Gmail account password
subject = "INFO TESIS PC-JULIO"
body = "SCRIPT EN CURSO LISTO"
 
# Endpoint for the SMTP Gmail server (Don't change this!)
smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
# Login with your Gmail account using SMTP
smtp_server.login(sender_address, account_password)
# Let's combine the subject and the body onto a single message
message = f"Subject: {subject}\n\n{body}"
# We'll be sending this message in the above format (Subject:...\n\nBody)
smtp_server.sendmail(sender_address, receiver_address, message)
# Close our endpoint
smtp_server.close()

