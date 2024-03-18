import requests
import json

session = requests.Session()

# login
data = {"username": 'ammar', "password": 'comp3011'}
header = {'Content-Type': 'application/x-www-form-urlencoded'}
r = session.post('http://127.0.0.1:8000/api/login', data=data, headers=header)
print(r.text)

# create story
data = {"headline": 'testing', "category": 'art', "region": 'eu', "details": 'testing new story'}
header = {'Content-Type': 'application/json'}
r = session.post('http://127.0.0.1:8000/api/stories', data=json.dumps(data), headers=header)
print(r.text)

# retrieve stories
r = session.get('http://127.0.0.1:8000/api/stories?story_cat=pol&story_region=w&story_date=01/03ds/2024')
if r.status_code != 200:
    print(r.text)
else:
    stories = r.json().get('stories')
    for story in stories:
        print(story)

# logout
r = session.post('http://127.0.0.1:8000/api/logout')
print(r.text)