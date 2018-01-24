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
 
 
class SavedTests(unittest.TestCase):
 
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
        )
 
    def login(self, username, password):
        return self.app.post(
                '/login',
                data=dict(username=username, password=password),
            )

    def create_theme(self, theme, inspire, author, time, token):
        return self.app.post(
                '/themeadmin',
                data=dict(theme=theme, theme_inspire=inspire, theme_author=author, release_time=time),
                headers=dict(Authorization="Bearer " + token)
                )

    def create_post(self, token, theme, anonymity, content):
        return self.app.post(
                '/posts',
                data=dict(theme=theme, anonymity=anonymity, content=content),
                headers=dict(Authorization="Bearer " + token)
                )

    def update_saved(self, mode, postid, token):
        return self.app.put(
                '/saved',
                data=dict(mode=mode, postid=postid),
                headers=dict(Authorization="Bearer " + token)
                )

 
    ###############
    #### tests ####
    ###############
    def test_valid_saved_append_delete(self):
        """
        tests appending a post to saved list of user, and incrementing
            1. Create two users
            2. Create a theme for the post
            3. Make a post written by the second user
            4. Add that post to saved
            5. Check by getting User and Post info that it has been added and incremented
        tests deleting a post from the saved list of user, and decrementing
            1. Delete post added.
            2. Check list and count that they are empty and 0
        """
        # register user mark 
        register_response = self.register('mark', '1018', 'who u?', 'me', 'hello')
        self.assertEqual(register_response.status_code, 201)

        # register user san
        register_response_san = self.register('san', '0', 'who u?', 'sanrtvflee', 'i love movies')
        self.assertEqual(register_response_san.status_code, 201)

        # login as mark
        login_response = self.login('mark', '1018')
        self.assertEqual(login_response.status_code, 200)
        login_response_data = json.loads(login_response.data.decode())
        self.assertEqual('Success!', login_response_data['message'])
        access_token_mark = login_response_data['access_token']
        self.assertTrue(access_token_mark)

        # login as mark
        login_response = self.login('san', '0')
        self.assertEqual(login_response.status_code, 200)
        login_response_data = json.loads(login_response.data.decode())
        self.assertEqual('Success!', login_response_data['message'])
        access_token_san = login_response_data['access_token']
        self.assertTrue(access_token_san)

        self.assertNotEqual(access_token_san, access_token_mark)

        # create theme
        theme_response = self.create_theme('love', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
        self.assertEqual(theme_response.status_code, 201)
        theme_data = json.loads(theme_response.data.decode())
        self.assertEqual('Success!', theme_data['message'])

        # make post by second user, san
        post_response = self.create_post(access_token_san, 'love', 'False', 'i love rtvf')
        self.assertEqual(post_response.status_code, 201)
        post_response_data = json.loads(post_response.data.decode())
        self.assertEqual('Success!', post_response_data['message'])

        # get post and check 'saved' count starts as 0
        get_by_theme = self.app.get(
                '/postlist/theme/love',
                headers=dict(Authorization="Bearer " + access_token_san)
                )
        self.assertEqual(get_by_theme.status_code, 200)
        get_by_theme_data = json.loads(get_by_theme.data.decode())
        san_post = get_by_theme_data['response'][0]
        self.assertEqual(san_post['writer_username'], 'san')
        self.assertEqual(san_post['saved'], 0)

        # update saved for user mark and san's post (mark saving san's post)
        saved_response = self.update_saved('append', '1', access_token_mark)
        self.assertEqual(saved_response.status_code, 200)

        # get post and check 'saved' count set as 1
        get_by_theme = self.app.get(
                '/postlist/theme/love',
                headers=dict(Authorization="Bearer " + access_token_san)
                )
        self.assertEqual(get_by_theme.status_code, 200)
        get_by_theme_data = json.loads(get_by_theme.data.decode())
        san_post = get_by_theme_data['response'][0]
        self.assertEqual(san_post['writer_username'], 'san')
        self.assertEqual(san_post['saved'], 1)

        # get user and check 'saved' list contains 1
        user_get = self.app.get(
                '/user/mark',
                headers=dict(Authorization="Bearer " + access_token_san),
                content_type='application/json'
                )
        self.assertEqual(user_get.status_code, 200)
        mark_data = json.loads(user_get.data.decode())['user']
        mark_saved_ls = mark_data['saved'].split(' ')
        self.assertEqual('1', mark_saved_ls[0])

        # check that repetition of the method is useless 
        saved_bad_response = self.update_saved('append', '1', access_token_mark)
        self.assertEqual(saved_bad_response.status_code, 500)
        saved_bad_data = json.loads(saved_bad_response.data.decode())
        self.assertEqual(saved_bad_data['message'], 'Already saved that post.')

        # check that the bad request had no effect
        get_by_theme = self.app.get(
                '/postlist/theme/love',
                headers=dict(Authorization="Bearer " + access_token_san)
                )
        self.assertEqual(get_by_theme.status_code, 200)
        get_by_theme_data = json.loads(get_by_theme.data.decode())
        san_post = get_by_theme_data['response'][0]
        self.assertEqual(san_post['writer_username'], 'san')
        self.assertEqual(san_post['saved'], 1)
        user_get = self.app.get(
                '/user/mark',
                headers=dict(Authorization="Bearer " + access_token_san),
                content_type='application/json'
                )
        self.assertEqual(user_get.status_code, 200)
        mark_data = json.loads(user_get.data.decode())['user']
        mark_saved_ls = mark_data['saved'].split(' ')
        self.assertEqual('1', mark_saved_ls[0])

        # update saved for user mark and san's post (mark delete
        saved_response = self.update_saved('delete', '1', access_token_mark)
        self.assertEqual(saved_response.status_code, 200)

        # check that delete decreased count for post and user
        get_by_theme = self.app.get(
                '/postlist/theme/love',
                headers=dict(Authorization="Bearer " + access_token_san)
                )
        self.assertEqual(get_by_theme.status_code, 200)
        get_by_theme_data = json.loads(get_by_theme.data.decode())
        san_post = get_by_theme_data['response'][0]
        self.assertEqual(san_post['writer_username'], 'san')
        self.assertEqual(san_post['saved'], 0)
        user_get = self.app.get(
                '/user/mark',
                headers=dict(Authorization="Bearer " + access_token_san),
                content_type='application/json'
                )
        self.assertEqual(user_get.status_code, 200)
        mark_data = json.loads(user_get.data.decode())['user']
        mark_saved_ls = mark_data['saved'].split(' ')
        self.assertEqual('', mark_saved_ls[0])

        

if __name__ == "__main__":
    unittest.main()

