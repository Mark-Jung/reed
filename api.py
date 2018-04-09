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


# create user mark, who is Admin
user_admin = requests.post(baseurl + "/register", data=json.dumps(admin_payload), headers=json_headers)
print('create admin: {0}'.format(user_admin.status_code))


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
        "theme": "themeMarch" + str(i+1),
        "theme_inspire": "inspire" + str(i+1),
        "theme_author": "author" + str(i+1)
    }
    new_theme = requests.post(baseurl + "/themeadmin", data=json.dumps(payload), headers=combined_headers)
    print('create new theme ' + str(i+1) + ': {0}'.format(new_theme.status_code))

# generate more themes for april
for i in range(28):
    payload = {
        "release_time": str(datetime(2018, 4, i+1, 20, 30, 00)),
        "theme": "themeApril" + str(i+1),
        "theme_inspire": "inspire" + str(i+1),
        "theme_author": "author" + str(i+1)
    }
    new_theme = requests.post(baseurl + "/themeadmin", data=json.dumps(payload), headers=combined_headers)
    print('create new theme ' + str(i+1) + ': {0}'.format(new_theme.status_code))

# create dummy users as client
for i in range(28):
    client_payload = {
        "username": "san" + str(i),
        "password": "0207",
        "question": "fav color",
        "answer": "orange",
        "intro": "hi I'm San" + str(i)
    }
    user_client = requests.post(baseurl + "/register", data=json.dumps(client_payload), headers=json_headers)
    print('created user: {0}'.format(user_client.status_code))

# let the admin post in march every other day
for i in range(28):
    if (i%2 == 0):
        payload = {
            "theme": "themeMarch" + str(i+1),
            "anonymity": "False",
            "content": "post by mark"
        }
        payload_april = {
            "theme": "themeApril" + str(i+1),
            "anonymity": "False",
            "content": "post by mark"
        }
        new_post = requests.post(baseurl + "/posts", data=json.dumps(payload), headers=combined_headers)
        new_post_april = requests.post(baseurl + "/posts", data=json.dumps(payload_april), headers=combined_headers)
        print('create new post ' + str(i+1) + ': {0}'.format(new_post.status_code))
        print('create new post ' + str(i+1) + ': {0}'.format(new_post_april.status_code))
        print(new_post.json())
        print(new_post_april.json())

tokens= []
for i in range(28):
    # client_payload = {
    #     "username": "san" + str(i),
    #     "password": "0207",
    #     "question": "fav color",
    #     "answer": "orange",
    #     "intro": "hi I'm San" + str(i)
    # }
    # user_client = requests.post(baseurl + "/register", data=json.dumps(client_payload), headers=json_headers)
    # print('created user: {0}'.format(user_client.status_code))
    login_payload = {
        "username": "san" + str(i),
        "password": "0207"
    }
    user_login = requests.post(baseurl + "/login", data=json.dumps(login_payload), headers=json_headers)
    non_admin_token = user_login.json()['access_token']
    combined_headers = {'Authorization': 'JWT ' + non_admin_token, 'content-type': 'application/json'}
    tokens.append(combined_headers)


for i in range(28):
    
    # let the admin post in march every other day
    for header in tokens:
        payload = {
            "theme": "themeMarch" + str(i+1),
            "anonymity": "False",
            "content": "post by user"
        }
        payload_april = {
            "theme": "themeApril" + str(i+1),
            "anonymity": "False",
            "content": "post by san" + str(i)
        }
        new_post = requests.post(baseurl + "/posts", data=json.dumps(payload), headers=header)
        new_post_april = requests.post(baseurl + "/posts", data=json.dumps(payload_april), headers=header)
        print('create new post ' + str(i+1) + ': {0}'.format(new_post.status_code))
        print('create new post ' + str(i+1) + ': {0}'.format(new_post_april.status_code))
        print(new_post.json())
        print(new_post_april.json())
