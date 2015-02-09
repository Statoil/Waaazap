import urllib2
import json
import datetime

stempel = datetime.datetime.now()
stempel_formatert = stempel.strftime('%Y-%m-%dT%H:%M:%SZ')
print(stempel_formatert)

data = {
    'device_id': 'mats sin pc',
    'timestamp': stempel_formatert,
    #'timestamp': '2015-02-09T13:55:00Z',
    'happyness_signal': 'happy'
}

req = urllib2.Request('http://127.0.0.1:8000/happyness_reg/')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(data).encode('ASCII'))

content = response.read()
