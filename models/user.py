from db import db

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    saved = db.Column(db.String(250))
    saved_count = db.Column(db.Integer)
    following = db.Column(db.String(250))
    following_count = db.Column(db.Integer)
    followed_by = db.Column(db.String(250))
    followed_by_count = db.Column(db.Integer)
    question = db.Column(db.String(100))
    answer = db.Column(db.String(40))
    intro = db.Column(db.String(20))


    def __init__(self, username, password, question, answer, intro):
        self.username = username
        self.password = password
        self.question = question
        self.answer = answer
        self.saved_count = 0
        self.intro = intro 

    def json(self):
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
