#!/usr/bin/env python3
import time
import requests
starttime=time.time()
messages=['Codigo']
id=''
for message in messages:
	localtime = time.asctime( time.localtime(time.time()) )
	mensaje = "Hora :" + localtime + "--" + message
	r=requests.post('https://api.telegram.org/bot<TOKEN>/sendMessage',
              data={'chat_id': id, 'text': mensaje})
	print(r.text)	
	time.sleep(10.0 - ((time.time() - starttime) % 10.0))
