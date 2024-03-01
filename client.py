import requests

r = requests.get('http://127.0.0.1:8000/api/greet')
print(r.text)