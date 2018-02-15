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

    def edit_theme(self, theme, inspire, author, time, token):
        return self.app.put(
                '/themeadmin',
                data=dict(theme=theme, theme_inspire=inspire, theme_author=author, release_time=time),
                headers=dict(Authorization="Bearer " + token)
                )
    def get_theme(self, mode, index, token):
        return self.app.get(
                '/theme/' + mode + '/' + index,
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
    """
    need to test:
        Done - create theme for the day: credentials, overlapping themes.
        Done - edit theme for the day, both early and late, but not after 5 minutes before release
        Not Done - check that the theme actually changes over time
    """
    def test_valid_create_theme(self):
        """
        check that no other user except for the admin is allowed access for and creating.
        """
        # register user mark
        register_response = self.register('mark', '1018', 'who u?', 'me', 'hello')
        self.assertEqual(register_response.status_code, 201)

        # register user san
        register_response = self.register('san', '1018', 'who u?', 'sanrtvflee', 'i love movies')
        self.assertEqual(register_response.status_code, 201)

        # login as mark
        login_response = self.login('mark', '1018')
        self.assertEqual(login_response.status_code, 200)
        login_response_data = json.loads(login_response.data.decode())
        self.assertEqual('Success!', login_response_data['message'])
        access_token_mark = login_response_data['access_token']
        self.assertTrue(access_token_mark)
        # login as san
        login_response = self.login('san', '1018')
        self.assertEqual(login_response.status_code, 200)
        login_response_data = json.loads(login_response.data.decode())
        self.assertEqual('Success!', login_response_data['message'])
        access_token_san = login_response_data['access_token']
        self.assertTrue(access_token_san)

        self.assertNotEqual(access_token_san, access_token_mark)

        # create theme -error1: non-admin create
        theme_create_error = self.create_theme('love', 'moi', 'mark', '2018-1-20 6:30:00', access_token_san)
        self.assertEqual(theme_create_error.status_code, 401)

        # make post by san with a theme that's not there. should return error.
        post_create_error = self.create_post(access_token_san, 'love', 'false', 'i love rtvf')
        self.assertEqual(post_create_error.status_code, 400)

        # create theme -error2: created at wrong time1, before 6:30 am
        theme_create_error = self.create_theme('love', 'moi', 'mark', '2018-1-20 2:30:00', access_token_san)
        self.assertEqual(theme_create_error.status_code, 401)

        # make post by san with a theme that's not there. should return error.
        post_create_error = self.create_post(access_token_san, 'love', 'false', 'i love rtvf')
        self.assertEqual(post_create_error.status_code, 400)

        # create theme -error3: created at wrong time2, before 8:30pm but after 6:30am
        theme_create_error = self.create_theme('love', 'moi', 'mark', '2018-1-20 10:31:23', access_token_san)
        self.assertEqual(theme_create_error.status_code, 401)

        # make post by san with a theme that's not there. should return error.
        post_create_error = self.create_post(access_token_san, 'love', 'false', 'i love rtvf')
        self.assertEqual(post_create_error.status_code, 400)

        # create theme -error4: created at wrong time3, after 8:30 am
        theme_create_error = self.create_theme('love', 'moi', 'mark', '2018-1-20 22:33:22', access_token_san)
        self.assertEqual(theme_create_error.status_code, 401)

        # make post by san with a theme that's not there. should return error.
        post_create_error = self.create_post(access_token_san, 'love', 'false', 'i love rtvf')
        self.assertEqual(post_create_error.status_code, 400)

        # create theme -valid early time
        theme_create_valid_early = self.create_theme('love', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
        self.assertEqual(theme_create_valid_early.status_code, 201)

        # make post by san -valid theme early
        post_create_valid = self.create_post(access_token_san, 'love', 'false', 'i love rtvf')
        self.assertEqual(post_create_valid.status_code, 201)

        # create theme -valid later time
        theme_create_valid_late = self.create_theme('coding', 'moi', 'mark', '2018-1-20 20:30:00', access_token_mark)
        self.assertEqual(theme_create_valid_late.status_code, 201)

        # make post by san -valid theme late
        post_create_valid = self.create_post(access_token_san, 'coding', 'false', 'i love rtvf')
        self.assertEqual(post_create_valid.status_code, 201)

        # create theme -invalid since overlapping theme
        theme_create_invalid_overlap = self.create_theme('coding', 'moi', 'mark', '2018-1-20 20:30:00', access_token_mark)
        self.assertEqual(theme_create_invalid_overlap.status_code, 400)

    def test_valid_theme_get(self):
        """
        scenarios to test for:
            theme changes after 6:30 am
            theme doesn't change for random times between 6:30 am and 8:30 pm
            theme chagnes after 8:30 pm
            theme doesn't change for randome times between 8:30 pm today and 6:30 am tmr
            If there is not theme for the assigned timed, it should return none.
        """
        # register user mark
        register_response = self.register('mark', '1018', 'who u?', 'me', 'hello')
        self.assertEqual(register_response.status_code, 201)

        # register user san
        register_response = self.register('san', '1018', 'who u?', 'sanrtvflee', 'i love movies')
        self.assertEqual(register_response.status_code, 201)

        login_and_create = datetime(2018, 2, 1, 6, 24, 0, 0)
        # freeze time for creating theme -valid early time
        with freeze_time(login_and_create):
            # login as mark
            login_response = self.login('mark', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_mark = login_response_data['access_token']
            self.assertTrue(access_token_mark)

            # create theme -valid early time
            theme_create_early = self.create_theme('marks', 'moi', 'mark', '2018-2-1 6:30:00', access_token_mark)
            self.assertEqual(theme_create_early.status_code, 201)
            # go 15 minutes later theme release
            theme_is_marks_time = datetime(2018, 2, 1, 6, 45, 0, 0)
            with freeze_time(theme_is_marks_time):
                get_theme_response = self.get_theme('now', '0', access_token_mark)
                self.assertEqual(get_theme_response.status_code, 200)
                get_theme_data = json.loads(get_theme_response.data.decode())
                self.assertEqual(get_theme_data['response'][0]['theme'], 'marks')
                self.assertEqual(get_theme_data['response'][0]['theme_inspire'], 'moi')
                self.assertEqual(get_theme_data['response'][0]['theme_author'], 'mark')
            for hour_delta in range(0, 13):
                for minute_delta in range(0, 60):
                    theme_still_marks_time = datetime(2018, 2, 1, hour_delta + 7, minute_delta, 0, 0)
                    with freeze_time(theme_still_marks_time):
                        get_theme_response = self.get_theme('now', '0', access_token_mark)
                        get_theme_data = json.loads(get_theme_response.data.decode())
                        self.assertEqual(get_theme_response.status_code, 200)
                        self.assertEqual(get_theme_data['response'][0]['theme'], 'marks')
                        self.assertEqual(get_theme_data['response'][0]['theme_inspire'], 'moi')
                        self.assertEqual(get_theme_data['response'][0]['theme_author'], 'mark')




    def test_valid_theme_edit(self):
        """
        scenarios to test for:
        Need to test if it was actually edited by using the get.
            6 minutes before release time -valid
                invalid release time for edit 
                invalid theme(overlapping)
                invalid credentials
            4 minutes before release time -invalid
            1 minute after release time -invalid
            
        """
        # register user mark
        register_response = self.register('mark', '1018', 'who u?', 'me', 'hello')
        self.assertEqual(register_response.status_code, 201)

        # register user san
        register_response = self.register('san', '1018', 'who u?', 'sanrtvflee', 'i love movies')
        self.assertEqual(register_response.status_code, 201)

        valid_early_edit_time = datetime(2018, 1, 20, 6, 24, 0, 0)
        # freeze time for creating theme -valid early time
        with freeze_time(valid_early_edit_time):
            # login as mark
            login_response = self.login('mark', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_mark = login_response_data['access_token']
            self.assertTrue(access_token_mark)

            # login as san
            login_response = self.login('san', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_san = login_response_data['access_token']

            # create theme -valid early time
            theme_create_early = self.create_theme('love', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
            self.assertEqual(theme_create_early.status_code, 201)
            """
            Check here with GET!!!!!
            """
        
            # create theme -valid late time
            theme_create_late = self.create_theme('coding', 'moi', 'mark', '2018-1-20 20:30:00', access_token_mark)
            self.assertEqual(theme_create_late.status_code, 201)
            """
            Check here with GET!!!!!
            """


            # edit theme -valid early time
            theme_edit_valid = self.edit_theme('peiru', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
            self.assertEqual(theme_edit_valid.status_code, 200)
            """
            Check here with GET!!!!!
            """
            # edit theme -valid early time
            theme_edit_valid = self.edit_theme('love', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
            self.assertEqual(theme_edit_valid.status_code, 200)
            """
            Check here with GET!!!!!
            """
            # invalid release_time
            theme_edit_invalid_release_time = self.edit_theme('peiru', 'moi', 'mark', '2018-1-30 8:30:00', access_token_mark)
            self.assertEqual(theme_edit_invalid_release_time.status_code, 400)
            """
            Check here with GET!!!!!
            """
            # invalid theme
            theme_edit_invalid_theme = self.edit_theme('coding', 'moi', 'mark', '2018-1-20 6:30:00', access_token_mark)
            self.assertEqual(theme_edit_invalid_theme.status_code, 400)
            """
            Check here with GET!!!!!
            """
            # invalid credentials
            theme_edit_invalid_credentials = self.edit_theme('coding', 'moi', 'mark', '2018-1-20 6:30:00', access_token_san)
            self.assertEqual(theme_edit_invalid_credentials.status_code, 401)
            """
            Check here with GET!!!!!
            """

        invalid_early_edit_time = datetime(2018, 1, 30, 6, 26, 0, 0)
        # freeze time for creating theme -valid early time
        with freeze_time(invalid_early_edit_time):
            # login as mark
            login_response = self.login('mark', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_mark = login_response_data['access_token']
            self.assertTrue(access_token_mark)

            # login as san
            login_response = self.login('san', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_san = login_response_data['access_token']

            # create theme -valid early time
            theme_create_early = self.create_theme('DFIR', 'moi', 'mark', '2018-1-30 6:30:00', access_token_mark)
            self.assertEqual(theme_create_early.status_code, 201)
            """
            Check here with GET!!!!!
            """

            # edit theme -invalid due to time
            invalid_theme_edit_early = self.edit_theme('love', 'moi', 'mark', '2018-1-30 6:30:00', access_token_mark)
            self.assertEqual(invalid_theme_edit_early.status_code, 400)
            """
            Check here with GET!!!!!
            """
        
        invalid_early_edit_time = datetime(2018, 1, 31, 6, 31, 0, 0)
        # freeze time for creating theme -valid early time
        with freeze_time(invalid_early_edit_time):
            # login as mark
            login_response = self.login('mark', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_mark = login_response_data['access_token']
            self.assertTrue(access_token_mark)

            # login as san
            login_response = self.login('san', '1018')
            self.assertEqual(login_response.status_code, 200)
            login_response_data = json.loads(login_response.data.decode())
            self.assertEqual('Success!', login_response_data['message'])
            access_token_san = login_response_data['access_token']

            # create theme -valid early time
            theme_create_early = self.create_theme('LOL', 'moi', 'mark', '2018-1-31 6:30:00', access_token_mark)
            self.assertEqual(theme_create_early.status_code, 201)

            # edit theme -invalid due to time
            invalid_theme_edit_late = self.edit_theme('love', 'moi', 'mark', '2018-1-31 6:30:00', access_token_mark)
            self.assertEqual(invalid_theme_edit_late.status_code, 400)
            """
            Check here with GET!!!!!
            """

        


        

if __name__ == "__main__":
    unittest.main()

