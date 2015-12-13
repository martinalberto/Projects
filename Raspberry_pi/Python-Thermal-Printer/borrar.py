#!/usr/bin/python

# Google Spreadsheet DHT Sensor Data-logging Example

# Depends on the 'gspread' package being installed.  If you have pip installed
# execute:
#   sudo pip install gspread

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import sys
import time
import datetime

import gspread

# Example of sensor connected to Beaglebone Black pin P8_11
#DHT_PIN  = 'P8_11'

# Google Docs account email, password, and spreadsheet name.
GDOCS_EMAIL            = '********@gmail.com'
GDOCS_PASSWORD         = '*******'
GDOCS_SPREADSHEET_NAME = 'your google docs spreadsheet name'

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 30


def login_open_sheet(email, password, spreadsheet):


		gc = gspread.login(email, password)
		#worksheet = gc.open(spreadsheet).sheet1
		#return worksheet

		print 'Unable to login and get spreadsheet.  Check email, password, spreadsheet name.'
		sys.exit(1)


print 'Logging sensor measurements to {0} every {1} seconds.'.format(GDOCS_SPREADSHEET_NAME, FREQUENCY_SECONDS)
print 'Press Ctrl-C to quit.'
worksheet = None
while True:
	# Login if necessary.
	if worksheet is None:
		worksheet = login_open_sheet(GDOCS_EMAIL, GDOCS_PASSWORD, GDOCS_SPREADSHEET_NAME)



 
	# Append the data in the spreadsheet, including a timestamp
	try:
		worksheet.append_row((datetime.datetime.now(), "a", "b"))
	except:
		# Error appending data, most likely because credentials are stale.
		# Null out the worksheet so a login is performed at the top of the loop.
		print 'Append error, logging in again'
		worksheet = None
		time.sleep(FREQUENCY_SECONDS)
		continue

	# Wait 30 seconds before continuing
	print 'Wrote a row to {0}'.format(GDOCS_SPREADSHEET_NAME)
	time.sleep(FREQUENCY_SECONDS)
