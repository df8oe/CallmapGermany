#!/usr/bin/env python
# -*- coding: utf-8 -*-
# By Ulrich Thiel, VK2UTL/DK1UT
import sys  
import sqlite3
import csv
from sets import Set

reload(sys)  
sys.setdefaultencoding('utf8')


dbconn = sqlite3.connect('calls.db')
dbcursor = dbconn.cursor()

#there are overlap locations so we proceed differently than in earlier versions
dbcursor.execute("SELECT Lng, Lat FROM Callsigns WHERE Geocode =1 GROUP BY Lat, Lng")
res = dbcursor.fetchall()

counter = 0
with open('calls-anon.csv', 'w') as csvfile:
    fieldnames = ['Lng', 'Lat', 'Label', 'Marker']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    
    for row in res:
    	lng = row[0]
    	lat = row[1]
    	dbcursor.execute("SELECT Id, Callsign, Class, Name, Street, Zip, City, Lng, Lat FROM Callsigns WHERE Lat="+str(lat)+" AND Lng= "+str(lng))
    	res = dbcursor.fetchall()
    	label = "<div class='googft-info-window'>"
    	classes = Set([])
    	
    	Acount = 0
    	Ecount = 0
    	for i in range(0,len(res)):
    		counter = counter + 1
    		current = res[i]
    		if current[2] == "A":
    			Acount = Acount + 1
    		else:
    			Ecount = Ecount + 1
    		classes.add(current[2])
    		#label = label + "<b>"+current[1]+" ("+current[3]+")</b><br>"
    		#label = label + current[4] + ", " + current[5] + " " + current[6]
    		#if i < len(res)-1:
    		#	label = label + "<br><br>"
    	
    	label = "Anzahl Stationen: " + str(len(res)) + " (" + str(Acount) + " A, " + str(Ecount) + " E)"
    	label = label + "<br><br>Anonymisierte Version, daher keine näheren Informationen sichtbar.<br>Für weitere Informationen siehe Rufzeichenliste<br>der BNetzA zu dieser Adresse oder siehe<br><a href=\"https://thielul.github.io/CallmapGermany/\">https://thielul.github.io/CallmapGermany/</a><br>zu Informationen zur Erstellung der vollständigen Karte"
    	
    	label = label + "</div>"
    	    	    		
    	if classes == Set(["A","E"]):
    		marker = "small_blue"
    	elif classes == Set(["A"]):
    		marker = "small_red"
    	elif classes == Set(["E"]):
    		marker = "small_purple"
    		
    	writer.writerow({'Lng':lng,'Lat':lat, 'Label':label, 'Marker':marker})

print counter

dbconn.close()