# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
try:
  import urllib.request as request
  import urllib.parse as parse
except ImportError:
  import urllib2 as request
  import urlparse as parse
import re
​
url = 'https://www.packtpub.com/packt/offers/free-learning'
subject = 'Packt Free Learning Daily Offer - '
​
def send_email(subject, message):
  msg = MIMEText(message)
  _from = '' #from email address
  _to = [''] #to email address, expected list object
  msg['Subject'] = '{}'.format(subject)
  msg['From'] = _from
  msg['To'] = _to[0] # only shows first _to email and others will be bcc
​
  # Send the message via our own SMTP server, but don't include the
  # envelope header.
  gmail_user = '@gmail.com' # any email address but I believe the settings are specific to gmail
  gmail_pwd = '' # email password (can use a secret.py file and import secret with these)
  smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465) #might change depending on host
  smtpserver.ehlo()
  smtpserver.ehlo
  smtpserver.login(gmail_user, gmail_pwd)
  smtpserver.sendmail(_from, _to, msg.as_string())
  smtpserver.quit()
  return'Email sent!'
​
page = request.urlopen(url)
soupysoupsoup = BeautifulSoup(page, 'lxml')
book_title = soupysoupsoup.find('div', class_='dotd-title').h2.text.encode('utf-8')
#direct_link = soupysoupsoup.findAll('div', class_={'float-left','free-ebook'})[-1].form.attrs['action'] #CAPTCHA prevents this being useful
description = [x for x in soupysoupsoup.find('div', class_ = {'dotd-main-book-summary'}).children][-4].get_text().strip().encode('utf-8')
​
book_title = re.sub(r'[\n\t]','', book_title)
message = '{}\n\n{}\n\n\nVisit Page: {}\n\n\n'.format(book_title,description, url)
subject += book_title
​
send_email(subject, message)