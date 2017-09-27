# use serverless on lambda architecture?

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
import ConfigParser

# for setting paramerisation (from https://wiki.python.org/moin/ConfigParserExamples)
def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = ConfigParser.ConfigParser()
Config.read("settings.ini")

FromEmail = ConfigSectionMap("Main")['fromemail']
Password = ConfigSectionMap("Main")['password']
ToEmail = ConfigSectionMap("Main")['toemail']
Url = ConfigSectionMap("Main")['url']
Subject = ConfigSectionMap("Main")['subject']

def send_email(subject, message):
  msg = MIMEText(message)
  _from = FromEmail
  _to = [ToEmail,''] #to email address, expected list object
  msg['Subject'] = '{}'.format(Subject)
  msg['From'] = _from
  msg['To'] = _to[0] # only shows first _to email and others will be bcc

  #  Send the message via our own SMTP server, but don't include the
  # envelope header.
  gmail_user = FromEmail # any email address but I believe the settings are specific to gmail
  gmail_pwd = Password # email password (can use a secret.py file and import secret with these)
  smtpserver = smtplib.SMTP_SSL("smtp.gmail.com",465) #might change depending on host
  smtpserver.ehlo()
  smtpserver.ehlo
  smtpserver.login(gmail_user, gmail_pwd)
  smtpserver.sendmail(_from, _to, msg.as_string())
  smtpserver.quit()
  return'Email sent!'

page = request.urlopen(Url)
soup = BeautifulSoup(page, 'lxml')
book_title = soup.find('div', class_='dotd-title').h2.text.encode('utf-8')
#direct_link = soup.findAll('div', class_={'float-left','free-ebook'})[-1].form.attrs['action'] #CAPTCHA prevents this being useful
description = [x for x in soup.find('div', class_ = {'dotd-main-book-summary'}).children][-4].get_text().strip().encode('utf-8')

book_title = re.sub(r'[\n\t]','', book_title)
Message = '{}\n\n{}\n\n\nVisit Page: {}\n\n\n'.format(book_title,description, Url)
Subject += book_title

send_email(Subject, Message)