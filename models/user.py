import os
from db import db
from flask_bcrypt import Bcrypt
from freezegun import freeze_time
import jwt
from datetime import datetime, timedelta

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    saved = db.Column(db.String(250))
    saved_count = db.Column(db.Integer)
    written = db.relationship(
            'PostModel', order_by="PostModel.date_created", cascade="all, delete-orphan")
    following = db.Column(db.String(250))
    following_count = db.Column(db.Integer)
    followed_by = db.Column(db.String(250))
    followed_by_count = db.Column(db.Integer)
    question = db.Column(db.String(100))
    answer = db.Column(db.String(40))
    intro = db.Column(db.String(20))


    def __init__(self, username, password, question, answer, intro):
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.question = question
        self.answer = answer
        self.saved_count = 0
        self.intro = intro
        self.following_count = 0
        self.followed_by_count = 0
       
    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def json(self):
        """
        Returns the json form of this model
        """
        return {'id': self.id, 'username': self.username, 'question': self.question, 'answer': self.answer, 'saved': self.saved, 'saved_count': self.saved_count, 'following_count': self.following_count, 'followed_by_count': self.followed_by_count, 'intro': self.intro, 'following': self.following, 'followed_by': self.followed_by}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def generate_token(self, _id):
        """ Generates the access token"""
        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(days=30),
                'iat': datetime.utcnow(),
                'sub': _id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_bytes = jwt.encode(
                payload,
                #'wjdrngusisthecreatorofreedforfun',
                os.environ['SECRET'],
                algorithm='HS256'
            )
            return jwt_bytes
        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def update_token(token):
        """
        Decodes the access token and if the expiration date is within 14 days,
        give them a 100 day extension
        """
        try:
            payload = jwt.decode(token, os.environ['SECRET'])
            payload['exp'] = datetime.utcnow() + timedelta(days=100)
            jwt_bytes = jwt.encode(
                    payload,
                    #'wjdrngusisthecreatorofreedforfun',
                    os.environ['SECRET'],
                    algorithm='HS256'
                    )
            return jwt_bytes
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            #payload = jwt.decode(token, 'wjdrngusisthecreatorofreedforfun')
            payload = jwt.decode(token, os.environ['SECRET'])
            return "", payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token", None
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login", None
