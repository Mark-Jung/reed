from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User
from resources.post import Post, PostList
from resources.saved import SavedUpdate
from resources.theme import Theme, ThemeAdmin, ThemeAdminGet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=2592000)
app.secret_key = 'reedforfun'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)  # /auth jwt creates this endpoint

api.add_resource(Post, '/posts')
api.add_resource(PostList, '/postlist/<string:mode>/<string:key>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:username>')
api.add_resource(SavedUpdate, '/saved/<string:mode>/<string:postid>')
api.add_resource(Theme, '/theme/<string:mode>/<int:index>')
api.add_resource(ThemeAdmin, '/themeadmin')
api.add_resource(ThemeAdminGet, '/adminget/<int:year>/<int:month>/<string:day>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)

