import requests
import json

session = requests.Session()
logged_in_url = None
url = None

def print_stories():
    print("\n\nGetting stories from " + url)
    r = session.get(f'{url}/api/stories?story_cat={cat}&story_region={reg}&story_date={date}')
    # error getting story
    if r.status_code != 200:
        print("Error " + str(r.status_code) + " getting stories from " + url + ".\n")
        # print error message if it is short, otherwise API has been poorly implemented 
        if (len(r.text) < 1000):
            print(r.text)
    # if stories are found
    else:
        for story in r.json().get('stories'):
            print(story.get('headline') + ", by " + story.get('author') + " : " + story.get('story_details') + "\n")

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
        r = session.post(f'https://{logged_in_url}/api/login', data=data, headers=header)
        print("\n" + r.text)
        
        
    if choice.lower() == "logout":
        if not session.cookies:
            print("You are not logged in.")
            continue
        r = session.post(f'https://{logged_in_url}/api/logout')
        # check if logout was successful and reset logged_in_url if so
        if r.status_code == 200:
            logged_in_url = None
        print("\n r.text")
        
        
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
        r = session.post(f'https://{logged_in_url}/api/stories', data=json.dumps(data), headers=header)
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
            
            print_stories()
        
        # if not specified, get the first 20 agencies
        else:
            agencies = agencies[:20]
            for a in agencies:
                url = a.get('url')
                print_stories()

        
    if choice.lower() == "list":
        r = session.get('http://newssites.pythonanywhere.com/api/directory')
        agencies = r.json()
        for a in agencies:
            print(a.get('agency_name') + " - " + a.get('url') + " - " + a.get('agency_code'))
    
    
    if choice.lower().startswith("delete"):
        if not session.cookies:
            print("You are not logged in.")
            continue
        story_id = choice.split(" ")[1]
        r = session.delete(f'https://{logged_in_url}/api/stories/{story_id}')
        print("\n" + r.text)
        