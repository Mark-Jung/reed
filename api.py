import requests
import datetime as dt
import json
from datetime import datetime

# type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),

baseurl = "http://127.0.0.1:5000/"
headers = {'content-type': 'application/json'}
payload = {
    "username": "mark" ,
    "password": "1018",
    "question": "fav color",
    "answer": "yellow",
    "intro": "hi I'm Mark"
}

# create user as Admin
user_admin = requests.post(baseurl + "register", data=json.dumps(payload), headers=headers)
print('create admin: {0}'.format(user_admin.status_code))

# create a theme
t_payload={
    "release_time": str(datetime(2018, 4, 6, 00, 00, 00)),
    "theme": 'fun',
    "theme_inspire": 'what is fun',
    "theme_author": 'life'
}
new_theme = requests.post(baseurl + "theme/create_theme", data=json.dumps(t_payload), headers=headers)
print('create new theme: {0}'.format(new_theme.status_code))
