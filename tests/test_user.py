import os, sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
basedir = os.path.abspath(os.path.dirname(__file__))
from app import app
from db import db
import json
 
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
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_valid_create_user(self):
        response = self.app.post(
                '/register',
                data=dict(username="mark", password="1018", question="who are you?", answer="i'm mark", intro="My name is ."),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 201)

    def test_overlapping_username_create_user(self):
        response = self.app.post(
                '/register',
                data=dict(username="mark", password="1018", question="who are you?", answer="i'm mark", intro="My name is ."),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 201)

        response = self.app.post(
                '/register',
                data=dict(username="mark", password="101", question="wh are you?", answer="im mark", intro="My name is "),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'The username is already taken', response.data)

    def test_incomplete_request_create_user(self):
        # missing intro
        response = self.app.post(
                '/register',
                data=dict(username="mark", password="101", question="who are you?", answer="I'm mark"),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This field is required and cannot be left blank.', response.data)
        # missing answer
        response = self.app.post(
                '/register',
                data=dict(username="mark", password="101", question="who are you?", intro="My name is ."),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This field is required and cannot be left blank.', response.data)
        # missing question
        response = self.app.post(
                '/register',
                data=dict(username="mark", password="101", answer="I'm mark", intro="My name is"),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This field is required and cannot be left blank.', response.data)
        # missing password 
        response = self.app.post(
                '/register',
                data=dict(username="mark", question="who are you?", answer="I'm mark", intro="My name is"),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This field is required and cannot be left blank.', response.data)
        # missing username 
        response = self.app.post(
                '/register',
                data=dict(password="101", question="who are you?", answer="I'm mark", intro="My name is"),
                follow_redirects=True
                )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'This field is required and cannot be left blank.', response.data)

    def test_invalid_login(self):
        """login with different credentials than the registration"""
        # valid registeration
        valid_register_response = self.app.post(
                '/register',
                data=dict(username="mark", password="1018", question="who are you?", answer="i'm mark", intro="My name is ."),
                follow_redirects=True
                )
        self.assertEqual(valid_register_response.status_code, 201)
        # login with unregistered credentials
        valid_login_response = self.app.post(
                '/login',
                data=dict(username="mark", password="101"),
                follow_redirects=True
                )
        self.assertEqual(valid_login_response.status_code, 401)

    def test_valid_login_and_token(self):
        """
        valid login should give token and success message
        """
        # valid registration
        valid_register_response = self.app.post(
                '/register',
                data=json.dumps(dict(username="mark", password="1018", question="who are you?", answer="i'm mark", intro="My name is .")),
                content_type='application/json'
                )
        self.assertEqual(valid_register_response.status_code, 201)
        # get valid token from valid login
        valid_login_response = self.app.post(
                '/login',
                data=dict(username="mark", password="1018"),
                follow_redirects=True
                )

        print(valid_login_response.data)
        
        self.assertEqual(valid_login_response.status_code, 200)
        valid_response_data = json.loads(valid_login_response.data.decode("utf-8"))
        self.assertEqual('Success!', valid_response_data['message'])
        self.assertTrue(valid_response_data['access_token'])
        access_token = valid_response_data['access_token']
        valid_user_get_response = self.app.get(
                '/user/mark',
                headers=dict(Authorization="Bearer " + access_token),
                content_type='application/json'
                )
        get_response_data = json.loads(valid_user_get_response.data.decode())
        if valid_user_get_response.status_code != 200:
            print(get_response_data['message'])

        self.assertTrue(get_response_data['user'])
        if get_response_data['user']:
            print("hi")
        #self.assertEqual(valid_user_get_response.status_code, 200)

    def test_invalidation_of_old_token(self):
        """
        old token should only last 1 more day
        INCOMPLETE. NEED TO FIND OUT HOW TO MANIPULATE TIME IN TESTING ENVIRONMENT
        """
        # valid registration
        valid_register_response = self.app.post(
                '/register',
                data=dict(username="mark", password="1018", question="who are you?", answer="i'm mark", intro="My name is ."),
                follow_redirects=True
                )
        self.assertEqual(valid_register_response.status_code, 201)
        """
        # get valid token from valid login
        valid_login_response = self.app.post(
                '/login',
                data=dict(username="mark", password="1018"),
                )
        self.assertEqual(valid_login_response.status_code, 200)
        valid_response_data = json.loads(valid_login_response.data.decode())
        self.assertEqual('Success!', valid_response_data['message'])
        """


if __name__ == "__main__":
    unittest.main()

