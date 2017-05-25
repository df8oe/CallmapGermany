#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By Ulrich Thiel, VK2UTL/DK1UT
#Adds coordinates to calls.db

import sqlite3
import geocoder
import requests
import sys
import time
from tqdm import tqdm

dbconn = sqlite3.connect('calls.db')
dbcursor = dbconn.cursor()

#For initial geocoding
dbcursor.execute("SELECT Id, Street, Zip, City FROM Callsigns WHERE Geocode IS NULL AND Street IS NOT NULL")

#For update geocoding
#dbcursor.execute("SELECT * FROM Callsigns WHERE Geocode = 0") 

res = dbcursor.fetchall()
print str(len(res)) + " addresses selected for geocoding"

#keep session alive
with requests.Session() as session:
	for i in tqdm(range(len(res))):
		row = res[i]
		address = row[1] + ", " + row[2] + " " + row[3] + ", Germany"
		#print address
		g = geocoder.google(address, session=session)
		#print g.status
		if g.status == 'OVER_QUERY_LIMIT':
			print "Query limit reached"
			sys.exit(0)
		if g.status == 'ZERO_RESULTS' or g.status == 'ERROR - No results found' or g.lng == None:
			dbcursor.execute("UPDATE Callsigns SET Geocode = 0 WHERE Id = " + str(row[0]))
		
		else:
			dbcursor.execute("UPDATE Callsigns SET Lng = " + str(g.lng) + ", Lat = " + str(g.lat) + ", Geocode = 1 WHERE Id = " + str(row[0]))
		dbconn.commit()
		
dbconn.close()
