#!/usr/bin/env python3
import time
import requests
starttime=time.time()
messages=['Codigo']
id='1657793959'
for message in messages:
	localtime = time.asctime( time.localtime(time.time()) )
	mensaje = "Hora :" + localtime + "--" + message
	r=requests.post('https://api.telegram.org/bot1460282614:AAF9GPKkPvhp0BD88BwuaMk_moYQbff9Zg4/sendMessage',
              data={'chat_id': id, 'text': mensaje})
	print(r.text)	
	time.sleep(10.0 - ((time.time() - starttime) % 10.0))
