import os, sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
from app import app
from db import db
import json
from datetime import datetime, timedelta
from freezegun import freeze_time
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.init_app(app)
        db.drop_all(app=app)
        db.create_all(app=app)
 
 
    # executed after each test
    def tearDown(self):
        pass
 
    ########################
    #### helper methods ####
    ########################
 
    def register(self, username, password, question, answer, intro):
        return self.app.post(
            '/register',
            data=dict(username=username, password=password, question=question, answer=answer, intro=intro),
            follow_redirects=True
        )
 
    def login(self, email, password):
        return self.app.post(
            '/auth',
            data=dict(username=username, password=password),
            follow_redirects=True
        )
 
    ###############
    #### tests ####
    ###############
    def test_valid_post_create(self):
        """
        tests if creating post is valid
            1. First creates theme.
            2. Second uploads post
            3. gets post by theme
        """
        #valid_post_response = self.app.post(
        #        '/route',
        #        follow_redirects=True
        #        )
        # create user mark
        register_response = self.app.post(
                '/register',
                data=dict(username="mark", password="1018", question="who are you", answer="I'm mark", intro="My name is ."),
                )
        self.assertEqual(register_response.status_code, 201)

        # login as mark
        login_response = self.app.post(
                '/login',
                data=dict(username="mark", password="1018")
                )
        self.assertEqual(login_response.status_code, 200)
        login_response_data = json.loads(login_response.data.decode())
        self.assertEqual('Success!', login_response_data['message'])
        access_token = login_response_data['access_token']
        self.assertTrue(access_token)

        # create theme
        theme_response = self.app.post(
                '/themeadmin',
                data=dict(theme="love", theme_inspire="moi", theme_author="mark", release_time="2018-1-20 6:30:00"),
                headers=dict(Authorization="Bearer " + access_token)
                )
        self.assertEqual(theme_response.status_code, 201)
        theme_data = json.loads(theme_response.data.decode())
        self.assertEqual('Success!', theme_data['message'])
        
        # upload post
        post_response = self.app.post(
                '/posts',
                data=dict(theme="love", anonymity="True", content="started with the bye and ended with a wrong hi"),
                headers=dict(Authorization="Bearer " + access_token)
                )
        self.assertEqual(post_response.status_code, 201)
        post_data = json.loads(post_response.data.decode())
        self.assertEqual('Success!', post_data['message'])

        # retrieve post by theme and check result

 


if __name__ == "__main__":
    unittest.main()

