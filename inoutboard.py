#!/usr/bin/python

import subprocess
import thread
import bluetooth
import time
import requests
import json
import os

API_KEY = 'VqxmF1tRVnFzGJpsg46AS19IHm5RJCM6'
rssi = None
threshold_off = -9
threshold_on = 0
in_a_row_on_limit = 0
in_a_row_off_limit = 5
in_a_row_on = 0
in_a_row_off = 0
sleep_time = 5

def pushMessage(title, body):
        data = {
                'type':'note',
                'title':title,
                'body':body
                }
        resp = requests.post('https://api.pushbullet.com/api/pushes',data=data, auth=(API_KEY,''))

def connect ():
	os.system("rfcomm conn CC:89:FD:5D:70:1A") 

print "In/Out Board"
thread.start_new_thread(connect, ())
time.sleep(10)

isHere = False
while True:
    rssi = None

    p = subprocess.Popen(['hcitool rssi CC:89:FD:5D:70:1A | sed \'s/^\RSSI return value:\s*//\''], stdout=subprocess.PIPE, shell=True)
    for line in iter(p.stdout.readline,''):
	rssi = int(line.rstrip())
	if(rssi >= threshold_on):
		in_a_row_on += 1
	else:
		in_a_row_on = 0
	if(rssi <= threshold_off):
		in_a_row_off += 1
	else:
		in_a_row_off = 0	
	

#   result = bluetooth.lookup_name('CC:89:FD:5D:70:1A', timeout=5)
    if (rssi != None and rssi >= threshold_on and in_a_row_on >= in_a_row_on_limit):
	if not isHere:
#		pushMessage("Jeff is in", "I just got Jeff on bluetooth")
		isHere = True
		os.system("codesend 4281651")     
    else:
	if (isHere and rssi != None and rssi <= threshold_off and in_a_row_off >= in_a_row_off_limit):
		isHere = False
#		pushMessage("Jeff has left", "I can't see him anymore")
		os.system("codesend 4281660")
    
    if(in_a_row_off > 0 or in_a_row_on > 0):
    	time.sleep(1)
    else:
	time.sleep(sleep_time)
