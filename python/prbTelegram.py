#!/usr/bin/python
# -*- coding: UTF-8 -*-
import telebot
bot = telebot.TeleBot("1460282614:AAF9GPKkPvhp0BD88BwuaMk_moYQbff9Zg4");

import requests
import os
import time
import sys

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


bot.polling()
