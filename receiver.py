import requests
import time
from datetime import datetime

def clean_message(message):
	dt = datetime.fromtimestamp(message['time'])
	dt_str = dt.strftime('%H:%M:%S')
	print(message['name'], dt_str)
	print(message['text'])
	print()

after = 0.0
while True:
	data = requests.get('http://127.0.0.1:5000/messages', params={'after': after}).json()
	for message in data['messages']:
		clean_message(message)
		after = message['time']
	time.sleep(1)