from db import db

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50))
    anonymity = db.Column(db.Boolean)
    username = db.Column(db.String(50))
    content = db.Column(db.String(200))
    saved = db.Column(db.Integer)

    def __init__(self, theme, anonymity, username, content):
        self.theme = theme
        self.anonymity = anonymity
        self.username = username
        self.content = content
        self.saved = 0

    def json(self):
        return {'id': self.id, 'theme': self.theme, 'anonymity': self.anonymity, 'username': self.username, 'content': self.content, 'saved': self.saved}

    @classmethod
    def filter_by_name(cls, username):
        return cls.query.filter_by(username=username).all()

    @classmethod
    def filter_by_theme(cls, theme):
        return cls.query.filter_by(theme=theme).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def increment_post_saved(cls, postid):
        try:
            target_post = PostModel.find_by_id(postid)
            target_post.saved += 1
            target_post.save_to_db()
            return ""
        except:
            return "Error while incrementing desired post's saved count"

    @classmethod
    def decrement_post_saved(cls, postid):
        try:
            target_post = PostModel.find_by_id(postid)
            if target_post.saved > 0:
                target_post.saved -= 1
            target_post.save_to_db()
            return ""
        except:
            return "Error while incrementing desired post's saved count"

