import requests
import json

session = requests.Session()

# login
data = {"username": 'ammar', "password": 'comp3011'}
header = {'Content-Type': 'application/x-www-form-urlencoded'}
r = session.post('http://127.0.0.1:8000/api/login', data=data, headers=header)
print(r.text)

# create story
data = {"headline": 'testing', "category": 'pol', "region": 'w', "details": 'testing new story'}
header = {'Content-Type': 'application/json'}
r = session.post('http://127.0.0.1:8000/api/stories', data=json.dumps(data), headers=header)
print(r.text)

# logout
r = session.post('http://127.0.0.1:8000/api/logout')
print(r.text)