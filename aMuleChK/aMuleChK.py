#!/usr/bin/env python
# -*- coding: utf-8 -*-
#### IMPORTS ####################
import sys
import os
import time, threading
#### LOG FILE ####
from io import open
#### AMULED ####
from subprocess import Popen, PIPE
import re
#### TELEGRAM ####
import telebot
import requests
#### WAVESHARE ####
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
from waveshare_epd import epd2in9bc
from PIL import Image,ImageDraw,ImageFont
import traceback
############  USER VARIABLES #############
from keys import token, user_id, user_path, user_txt, aMulepass, aMulelogo, avatar
############### FUNCTIONS      ###############

#### TELEGRAM FUNCTIONS ####
bot = telebot.TeleBot(token);

@bot.message_handler(func=lambda message: message.text.lower() == 'id')
def saludar(message):
	firstName = message.chat.first_name
	bot.send_message(message.chat.id, "Hola {} tu ID es: {}".format(firstName,message.chat.id))
	txtToFile("Hola {} tu ID es: {}".format(firstName,message.chat.id))
	
@bot.message_handler(func=lambda message: message.text.lower() == 'activo')
def amuledActivated(message):
	localTime = time.asctime( time.localtime(time.time()) )
	if activated():
		status = 'amuled activo.'
	else:
		status = '¡amuled NO está funcionando!'
	firstName = message.chat.first_name
	bot.send_message(message.chat.id, "Hola {}, {} {}".format(firstName, status, localTime))
	txtToFile("Hola {}, {} {}".format(firstName, status, localTime))

@bot.message_handler(func=lambda message: message.text[:len("mensaje")].lower() == 'mensaje' and message.chat.id == user_id)
def command_long_text(message):
    cid = message.chat.id
    firstName = message.chat.first_name
    bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    txtMessage = formatMessage(message.text[len("mensaje"):])
    txtToDisplay(txtMessage, 10, avatar)
    bot.send_message(cid, "Mensaje enviado")
    txtToFile("Mensaje \"{}\" enviado a display por {} Id: {}".format(txtMessage, firstName, cid))

@bot.message_handler(func=lambda message: message.text[:len("run")].lower() == 'run' and message.chat.id == user_id)
def execCommand(message):
	cid = message.chat.id
	firstName = message.chat.first_name
	time.sleep(2)
	aMuleCommand = formatMessage(message.text[len("run"):])
	aMuleExit = os.popen(aMuleCommand).read()
	bot.send_message(cid, "Comando ejecutado con salida:")
	bot.send_message(cid, aMuleExit)
	txtToFile("Comando {} ejecutado por usuario {} con respuesta:\n {}".format(aMuleCommand, firstName, aMuleExit))
    
def messageToTelegram(message):
	bot.send_message(user_id, message)
	
def formatMessage(txt):
	if len(txt) > 27:
		words = re.split(' ',txt)
		length = 0
		returnTxt = ''
		for word in words:
			length += len(word)
			if length < 27:
				returnTxt = returnTxt + word + ' '
			else:
				returnTxt = returnTxt + '\n'+ word + ' '
				length = len(word)
				
	else:
		returnTxt = txt
	
	return returnTxt

def controlBot():
	print ('bot waiting instructions...')
	bot.polling()
	
#### AMULED FUNCTIONS ####
def activated():
	aMuleCommand ='ps -C amuled'
	aMuleExit = os.popen(aMuleCommand).read()
	aMuleReturn = re.split('\n',aMuleExit)[1:]
	if len(aMuleReturn)==1:
		return False
	else:
		return True
		
def launcher():
	if not activated():
		aMuleCommand = 'su - ' + user_txt + ' -c "amuled -f"'
		aMuleExit = os.popen(aMuleCommand).read()
	time.sleep(10)

def state():
	aMuleCommand = 'amulecmd -P ' + aMulepass + ' -c status'
	aMuleExit = os.popen(aMuleCommand).read()
	aMuleReturn = re.split('\n > ', aMuleExit)[1:]
	aMuleReturn [-1]= re.split('\n', aMuleReturn[-1])[0]
	print (aMuleReturn[0] + '..' + aMuleReturn[1] + '..' + 
			aMuleReturn[2] + '..' + aMuleReturn[3])
	return (aMuleReturn[0], aMuleReturn[1], 
			aMuleReturn[2], aMuleReturn[3])
	

#### WAVESHARE FUNCTIONS ####
def sleepMode():
	try:
		logging.info("A dormir...")
		epd.sleep()
		time.sleep(3)
		epd.Dev_exit()
	
	except IOError as e:
		logging.info(e)
		
	except KeyboardInterrupt:    
		logging.info("ctrl + c:")
		epd2in9bc.epdconfig.module_exit()
		exit()
	
def txtToDisplay(txt,fontSize,img):	
	try:
		epd = epd2in9bc.EPD()
		epd.init()
		epd.Clear()

		#rectangle
		HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
		drawblack = ImageDraw.Draw(HBlackimage)
		drawblack.rectangle((100, 4, 292, 124), outline = 0)
		#text
		fontCustom = ImageFont.truetype(os.path.join(picdir, 'DejaVuSans.ttf'), fontSize)
		drawblack.text((105,9 ), txt, font = fontCustom, fill = 0)
		#logo
		HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
		logo = Image.open(os.path.join(picdir, img))
		HRYimage.paste(logo, (0,0))
		
		epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
		
		epd.sleep()
		time.sleep(3)
	
	except IOError as e:
		logging.info(e)
		
	except KeyboardInterrupt:    
		logging.info("ctrl + c:")
		epd2in9bc.epdconfig.module_exit()
		exit()

def updateDisplay():
	aMuleData = state()
	serverName = re.split(' ', aMuleData[0])[1:]
	last = len(serverName)-1
	serverTxt = serverName[2].strip() + ' '
	if ((serverName[3])[:1] != '['):
		serverTxt += serverName[3].strip() + ' '
	serverTxt += 'con ' + serverName[last].strip()
	#Kademlia status
	if (aMuleData[1])[16:18].strip() == 'fi':
		kademliaTxt = 'Tras cortafuegos'
	else:
		kademliaTxt = (aMuleData[1])[16:18].strip()
	#download speed
	downloadTxt = (aMuleData[2])[9:].strip()
	#upload speed
	uploadTxt = (aMuleData[3])[8:].strip()
	actualTime = time.strftime("%H:%M:%S")
	txtFormated = ("Hora de la consulta: {} \nServidor: {} \nKademlia: {} \nDownload: {} \nUpload: {}"
				  .format(actualTime, serverTxt, kademliaTxt,
				  downloadTxt, uploadTxt))
	txtToDisplay(txtFormated, 10, aMulelogo)
	txtToFile("{}. Download: {}. Upload: {}".format(serverTxt, downloadTxt, uploadTxt))
	
def controlDisplay():
	if activated():
		#get the aMule status and wait for conected to server status
		status = "Now"
		while status == "Now":
			aMuleData = state()
			serverName = re.split(' ', aMuleData[0])[1:]
			status = serverName[0]
		#check the status of amuled every 60 minutes at night
		#and every 15 minutes at day
		while True:
			updateDisplay()
			actualTime = time.strftime("%H")
			if (actualTime > '21'):
				time.sleep(3600)
			else:
				time.sleep(900)
	else:
		print ('writing to display...')
		serverTxt = '!aMuled NO está activo¡'
		txtToDisplay(serverTxt, 12, aMulelogo)
		messageToTelegram(serverTxt)
		txtToFile(serverTxt)

#### LOG FUNCTIONS ####
def txtToFile(txt):
	actualTime = time.strftime("%H:%M:%S")
	actualDate = time.strftime("%Y%m%d")
	txtFormated = "{}: {}.\n".format(actualTime, txt)
	logFile = open ('/home/aMuleChK/aMuleChK/logFile_' + actualDate + '.txt','a+')
	logFile.write(txtFormated)
	logFile.close()
	
#### MAIN PROCESS ####	
def main():	
	launcher()
	threadDisplay = threading.Thread(target = controlDisplay)
	threadDisplay.start()
	threadBot = threading.Thread(target = controlBot)
	threadBot.start()
	
		
#### aMuleChk ####
if __name__ == '__main__':
	main()
