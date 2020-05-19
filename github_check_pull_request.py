import requests, json
from datetime import datetime, timedelta
import os

#vietjovi@gmail.com

repo = 'vietjovi/integrate-sonarqube-github'
project = 'integrate-sonarqube-github'
token = 'YOUR_PERSONAL_TOKEN'
last = ''

headers = {'Authorization': 'token %s' % token}
response = requests.get('https://api.github.com/repos/'+repo+'/pulls', headers=headers)

#the file "last" will contain the last pull request's branch
with open("last", "r") as f:
	last = f.read() 

print(last)
data = json.loads(response.text)

if ((data[0]['state'] == 'open') and (last != data[0]['head']['ref'])):
	print(data[0]['head']['ref'])
	print(data[0]['created_at'])
	eventTime = datetime.strptime(data[0]['created_at'], '%Y-%m-%dT%H:%M:%SZ')
	print(eventTime)
	with open("last", "w") as f:
		last = f.write(data[0]['head']['ref'])
	print("Proccessing!")
	open('scanning.pid', 'a').close()
	stream = os.popen('git clone --single-branch --branch '+data[0]['head']['ref']+' git@github.com:'+repo+'.git')
	output = stream.read()
	print(output)
