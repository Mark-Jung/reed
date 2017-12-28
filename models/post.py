from db import db
from models.user import UserModel
from sqlalchemy import desc

class PostModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(50))
    anonymity = db.Column(db.Boolean)
    content = db.Column(db.String(200))
    saved = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    writer = db.Column(db.Integer, db.ForeignKey(UserModel.id))

    def __init__(self, theme, anonymity, writer, content):
        self.theme = theme
        self.anonymity = anonymity
        self.writer = writer 
        self.content = content
        self.saved = 0

    def json(self):
        return {'id': self.id, 'theme': self.theme, 'anonymity': self.anonymity, 'writer_username': UserModel.find_by_id(self.created_by).username, 'writer_id': self.writer, 'content': self.content, 'saved': self.saved}

    @classmethod
    def filter_by_writer(cls, writer):
        return cls.query.filter_by(writer=writer).all()

    @classmethod
    def filter_by_theme(cls, theme):
        return cls.query.filter_by(theme=theme).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def filter_by_most_saved(cls):
        return cls.query.order_by(desc(PostModel.saved)).all()

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

