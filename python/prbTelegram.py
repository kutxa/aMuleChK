#!/usr/bin/python
# -*- coding: UTF-8 -*-
import telebot
bot = telebot.TeleBot("1460282614:AAF9GPKkPvhp0BD88BwuaMk_moYQbff9Zg4");

import requests
import os
import time
import sys
from subprocess import Popen, PIPE
import re

owner = 1657793959

@bot.message_handler(func=lambda message: message.text.lower() == 'id')
def saludar(message):
	firstName = message.chat.first_name
	bot.send_message(message.chat.id, "Hola {} tu ID es: {}".format(firstName,message.chat.id))

#Mandas la palabra ip y te devuelve la ip
@bot.message_handler(func=lambda message: message.text.lower() == 'ip' and message.chat.id == owner)
def miip(message):
    ip = requests.get("http://ipinfo.io/ip")
    bot.send_message(message.chat.id, "IP: {}".format(ip.text));
 
##Mandas la palabra temperatura y te devuelve la temperatura
@bot.message_handler(func=lambda message: message.text.lower() == 'temperatura' and message.chat.id == owner)
def temperatura(message):
    temp    = round(int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3, 2)
    bot.send_message(message.chat.id, "Temperatura de la CPU: {} °C".format(temp));
    

@bot.message_handler(func=lambda message: message.text.lower() == 'versión' and message.chat.id == owner)
def version(message):
    version = sys.version
    bot.send_message(message.chat.id, "Versión: {}".format(version));
    
@bot.message_handler(func=lambda message: message.text.lower() == 'run' and message.chat.id == owner)
def name_script(message):
    name = sys.argv[0]
    bot.send_message(message.chat.id, "Running: {}".format(name));

@bot.message_handler(func=lambda message: message.text.lower() == 'usb' and message.chat.id == owner)
def usbList(message):
	command = 'lsusb'
	txtExit = os.popen(command).read()
	listUsb = re.split('\n',txtExit)
	exitUsb = ""
	for usb in listUsb:
		exitUsb += "{}\n".format(usb[33:])
	bot.send_message(message.chat.id, "USB connections: \n{}".format(exitUsb));
	
@bot.message_handler(func=lambda message: message.text[:len("exec")].lower() == 'exec' and message.chat.id == owner)
def command_long_text(message):
    cid = message.chat.id
    bot.send_message(cid, "Ejecutando: "+ message.text[len("exec"):])
    bot.send_chat_action(cid, 'typing') # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    f = os.popen(message.text[len("exec"):])
    result = f.read()
    bot.send_message(cid, "Resultado: " + result)
	


bot.polling()
