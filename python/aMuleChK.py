#!/usr/bin/env python
# -*- coding: utf-8 -*-
#### IMPORTS ####################
#### AMULED ####
import sys, os
from subprocess import Popen, PIPE
import re
#### WAVESHARE ####
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in9bc
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
############  USER VARIABLES #############
from keys import token, user_id, user_path
############### FUNCTIONS      ###############
def activated():
	aMuleCommand ='ps -C amuled'
	aMuleExit = os.popen(aMuleCommand).read()
	aMuleExit = aMuleExit.decode()
	aMuleReturn = re.split('\n',aMuleExit)[1:]
	if len(aMuleReturn)==1:
		return False
	else:
		return True

def state():
	aMuleCommand = 'amulecmd -c status'
	aMuleExit = os.popen(aMuleCommand).read()
	aMuleExit = aMuleExit.decode()
	aMuleReturn = re.split('\n > ', aMuleExit)[1:]
	aMuleReturn[-1 = re.split('\n', aMuleReturn[-1])[0]
	return (aMuleReturn[0], aMuleReturn[1], 
			aMuleReturn[2], aMuleReturn[3])
	
def launcher(event):
	if not activated():
		aMuleCommand = 'amuled -f'
		aMuleExit = os.popen(aMuleCommand).read()
	sleep(4)
	
def main():
	launcher()
	if activated():
		#get the aMule status
		aMuleData = state()
		#server name
		serverName = re.split(' ', aMuleData[0])[1:]
		serverTxt = serverName[2].strip() + ' ' + serverName[5].strip())
		#Kademlia status
		if (aMuleData[1])[16:18].strip()=='fi':
			kademliaTxt = 'Red Kademlia tras cortafuegos'
		else:
			kademliaTxt = (aMuleData[1])[16:18].strip()
			#download speed
			downloadTXT = (aMuleData[2])[9:].strip()
			#upload speed
			uploadTxt = (aMuleData[3])[8:].strip()		
		else:
			serverTxt = '!aMuled NO está activo¡'
	









##########   PRINCIPAL  ######################
if __name__ == '__main__':
	main()
