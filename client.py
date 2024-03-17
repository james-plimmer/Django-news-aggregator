import requests

data = {"username": 'ammar', "password": 'comp3011'}
header = {'Content-Type': 'application/x-www-form-urlencoded'}
r = requests.post('http://127.0.0.1:8000/api/login', data=data, headers=header)
print(r.text)
r = requests.post('http://127.0.0.1:8000/api/logout')
print(r.text)