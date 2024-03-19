import requests
import json

session = requests.Session()

# # login
# data = {"username": 'ammar', "password": 'comp3011'}
# header = {'Content-Type': 'application/x-www-form-urlencoded'}
# r = session.post('http://127.0.0.1:8000/api/login', data=data, headers=header)
# print(r.text)

# # create story
# data = {"headline": 'testing', "category": 'art', "region": 'eu', "details": 'testing new story'}
# header = {'Content-Type': 'application/json'}
# r = session.post('http://127.0.0.1:8000/api/stories', data=json.dumps(data), headers=header)
# print(r.text)

# # delete a story
# r = session.delete('http://127.0.0.1:8000/api/stories')
# print(r.text)

# # retrieve stories
# r = session.get('http://127.0.0.1:8000/api/stories?story_cat=*&story_region=*&story_date=*')
# if r.status_code != 200:
#     print(r.text)
# else:
#     stories = r.json().get('stories')
#     for story in stories:
#         print(story)

# # logout
# r = session.post('http://127.0.0.1:8000/api/logout')
# print(r.text)

session = requests.Session()
logged_in_url = None
url = None

while True:
    print("\n\n\n------")
    print("login <url>")
    print("logout")
    print("post")
    print("news[-id=][-cat=][-reg=][-date=]")
    print("list")
    print("delete <story_key>")
    print("Enter Q to exit.")
    print("------")
    choice = input("Enter a command: ")
    print("\n\n\n")
    
    if choice.upper() == "Q":
        break


    if choice.lower().startswith("login") and len(choice.split(" ")) == 2:
            
        logged_in_url = choice.split(" ")[1]
        username = input("Enter username: ")
        password = input("Enter password: ")
        data = {"username": username, "password": password}
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = session.post(f'{logged_in_url}/api/login', data=data, headers=header)
        print("\n" + r.text)
        
        
    if choice.lower() == "logout":
        if not session.cookies:
            print("You are not logged in.")
            continue
        r = session.post(f'{logged_in_url}/api/logout')
        logged_in_url = None
        print("\nLogged out.")
        
        
    if choice.lower() == "post":
        if not session.cookies:
            print("You are not logged in.")
            continue
        headline = input("Enter headline: ")
        category = input("Enter category: ")
        region = input("Enter region: ")
        details = input("Enter details: ")
        data = {"headline": headline, "category": category, "region": region, "details": details}
        header = {'Content-Type': 'application/json'}
        r = session.post(f'{logged_in_url}/api/stories', data=json.dumps(data), headers=header)
        print("\n" + r.text)
        
        
    if choice.lower().startswith("news"):
        # parse switches
        switches = {}
        for s in choice.split():
            if s.startswith("-"):
                new_s = s.split("=")
                if (new_s[0][1:] not in ["id", "cat", "reg", "date"]):
                    print(f"Invalid switch: {s.split('=')[0][1:]}")
                    continue
                if (new_s[0][1:] in switches):
                    print(f"Duplicate switch: {s.split('=')[0][1:]}")
                    continue
                
                switches[s.split("=")[0][1:]] = s.split("=")[1]
        
        # set defaults
        # get all agencies
        r = session.get('http://newssites.pythonanywhere.com/api/directory')
        agencies = r.json()
        cat = '*'
        reg = '*'
        date = '*'
        
        # array to store stories
        stories = []
        
        # check for switch presence and set values
        # switch validation is done server-side
        if 'cat' in switches.keys():
            cat = switches['cat']
        if 'reg' in switches.keys():
            reg = switches['reg']
        if 'date' in switches.keys():
            date = switches['date']

        # if agency is specified
        if 'id' in switches.keys():
            # get url from agency id
            for a in agencies:
                if a.get('agency_code') == switches['id']:
                    url = a.get('url')
                    break
                # check that an agency was found   
            if not url:
                print("Invalid agency code.")
                continue
            
            print("\n\nGetting stories from " + url)
            r = session.get(f'{url}/api/stories?story_cat={cat}&story_region={reg}&story_date={date}')
            for story in r.json().get('stories'):
                print(story.get('headline'))
        
        # if not specified, get the first 20 agencies
        else:
            count = 0
            for a in agencies:
                stories = []
                url = a.get('url')
                print("\n\nGetting stories from " + url)
                r = session.get(f'{url}/api/stories?story_cat={cat}&story_region={reg}&story_date={date}')
                if r.status_code != 200:
                    print(r.text)
                    count += 1
                    if count == 20:
                        break
                    continue
                
                if r.json().get('stories') != None:
                    try:
                        for story in r.json().get('stories'):
                            print(story.get('headline'))
                    except json.JSONDecodeError:
                        print("\n\nError getting stories.")
                
                count += 1
                if count == 20:
                    break
        
    if choice.lower() == "list":
        r = session.get('http://newssites.pythonanywhere.com/api/directory')
        agencies = r.json()
        for a in agencies:
            print(a.get('agency_name') + " " + a.get('url') + " " + a.get('agency_code'))
    
    
    if choice.lower().startswith("delete"):
        if not session.cookies:
            print("You are not logged in.")
            continue
        story_id = choice.split(" ")[1]
        r = session.delete(f'{logged_in_url}/api/stories/{story_id}')
        print("\n" + r.text)
        