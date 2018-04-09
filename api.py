import requests
import datetime as dt
import json
from datetime import datetime
from db import db
from models.user import UserModel

# type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),

baseurl = "http://127.0.0.1:5000"

json_headers = {'content-type': 'application/json'}
admin_payload = {
    "username": "mark",
    "password": "1018",
    "question": "fav color",
    "answer": "yellow",
    "intro": "hi I'm Mark"
}


# create user as Admin
user_admin = requests.post(baseurl + "/register", data=json.dumps(admin_payload), headers=json_headers)
print('create admin: {0}'.format(user_admin.status_code))

# create user as client
client_payload = {
    "username": "san",
    "password": "0207",
    "question": "fav color",
    "answer": "orange",
    "intro": "hi I'm San"
}
user_client = requests.post(baseurl + "/register", data=json.dumps(client_payload), headers=json_headers)
print('create admin: {0}'.format(user_client.status_code))

# log in as Admin for access_token
admin_credential = {
    "username": "mark",
    "password": "1018"
}
login_admin = requests.post(baseurl + "/login", data=json.dumps(admin_credential), headers=json_headers)
print('login admin: {0}'.format(login_admin.status_code))
jwt_token = login_admin.json()['access_token']

# create a theme as Admin
combined_headers = {'Authorization': 'JWT ' + jwt_token, 'content-type': 'application/json'}

t1_payload = {
    "release_time": str(datetime(2018, 4, 6, 20, 30, 00)),
    "theme": "fun",
    "theme_inspire": "what is fun",
    "theme_author": "life"
}
new_theme = requests.post(baseurl + "/themeadmin", data=json.dumps(t1_payload), headers=combined_headers)
print(new_theme.json())
print('create new theme one: {0}'.format(new_theme.status_code))

# generate more themes for march
for i in range(30):
    payload = {
        "release_time": str(datetime(2018, 3, i+1, 20, 30, 00)),
        "theme": "theme_march" + str(i+1),
        "theme_inspire": "inspire" + str(i+1),
        "theme_author": "author" + str(i+1)
    }
    new_theme = requests.post(baseurl + "/themeadmin", data=json.dumps(payload), headers=combined_headers)
    print('create new theme ' + str(i+1) + ': {0}'.format(new_theme.status_code))

# generate more themes for april
for i in range(5):
    payload = {
        "release_time": str(datetime(2018, 4, i+1, 20, 30, 00)),
        "theme": "theme_april" + str(i+1),
        "theme_inspire": "inspire" + str(i+1),
        "theme_author": "author" + str(i+1)
    }
    new_theme = requests.post(baseurl + "/themeadmin", data=json.dumps(payload), headers=combined_headers)
    print('create new theme ' + str(i+1) + ': {0}'.format(new_theme.status_code))


# let the admin post in march every other day
for i in range(30):
    if (i%2 == 0):
        payload = {
            "theme": "theme_march" + str(i+1),
            "anonymity": "True",
            # "writer_id": str(UserModel.find_by_username('mark').query.with_entities(UserModel.id)),
            "writer_id": "2",
            "content": "post by mark"
        }
        print(payload)
        new_post = requests.post(baseurl + "/posts", data=json.dumps(payload), headers=combined_headers)
        print('create new post ' + str(i+1) + ': {0}'.format(new_post.status_code))
        print(new_post.json())
