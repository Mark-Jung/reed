from db import db
from sqlalchemy import desc

class ThemeModel(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    release_time = db.Column(db.DateTime)
    theme = db.Column(db.String(50))
    theme_inspire = db.Column(db.String(250))
    theme_author = db.Column(db.String(50))
    picture_link = db.Column(db.String(250))
    picture_description = db.Column(db.String(250))
    picture_artist = db.Column(db.String(50))

    def __init__(self, release_time, theme, theme_inspire, theme_author):
        self.release_time = release_time
        self.theme = theme
        self.theme_inspire = theme_inspire
        self.theme_author = theme_author

    def json(self):
        return {'release_time': self.release_time.strftime("%Y-%m-%d %H:%M:%S"), 'theme': self.theme, 'theme_inspire': self.theme_inspire, 'theme_author': self.theme_author}

    @classmethod
    def find_by_theme(cls, theme):
        return cls.query.filter_by(theme=theme).first()

    @classmethod
    def find_by_theme_author(cls, theme_author):
        return cls.query.filter_by(theme_author=theme_author).all()

    @classmethod
    def find_by_release_time(cls, current_time):
        return cls.query.filter_by(release_time=current_time).first()

    @classmethod
    def list_between_by_release_time(cls, lowbound_time, highbound_time, limit):
        return cls.query.filter(cls.release_time <= highbound_time, cls.release_time >= lowbound_time).order_by(desc(cls.release_time)).limit(limit).all()

    @classmethod
    def get_count(cls, current_time):
        return cls.query.filter(cls.release_time <= current_time).count()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
