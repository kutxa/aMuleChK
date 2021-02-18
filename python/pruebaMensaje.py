#!/usr/bin/env python3
import requests
id='1657793959'
r=requests.post('https://api.telegram.org/bot1460282614:AAF9GPKkPvhp0BD88BwuaMk_moYQbff9Zg4/sendMessage',
              data={'chat_id': id, 'text': 'Prueba de texto desde Python 2ª parte'})
print(r.text)
