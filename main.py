import os
import argparse
import datetime

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Get the arguments
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-u", "--url", required=True, help="url to test")
arg_parser.add_argument("-e", "--emails", required=True, help="comma separated list of emails to notify")
arg_parser.add_argument("-a", "--notify-always", action='store_true', help="when present, will send an email even if test was successful")
args = vars(arg_parser.parse_args())
url = args["url"]
emails = args["emails"].split(",")
notify_always = args["notify_always"]

# Make the request
response = requests.get(url)

# Report on the results (email)
email_subject = ""
readable_url = url.split('://')[1]
if response.status_code > 500:
    email_subject = f"❌ {readable_url} is down"
elif notify_always:
    email_subject = f"✅ {readable_url} is up"
if not email_subject:
    exit()

# Get email host config
email_host = os.environ["EMAIL_HOST"]
email_port = os.environ["EMAIL_PORT"]
email_host_user = os.environ["EMAIL_HOST_USER"]
email_host_password = os.environ["EMAIL_HOST_PASSWORD"]

# Send email
email_text = f"{url} returned a status code of {response.status_code} at {datetime.datetime.now()}"
sender_email = "http-up-check@phiture.com"
message = MIMEMultipart()
message["From"] = sender_email
message["Subject"] = email_subject
message.attach(MIMEText(email_text, "plain"))
with smtplib.SMTP(email_host, email_port) as server:
    server.login(email_host_user, email_host_password)
    for email in emails:
        message["To"] = email
        text = message.as_string()
        server.sendmail(sender_email, email, text)
