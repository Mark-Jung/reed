from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field is required and cannot be left blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field is required and cannot be left blank."
    )
    parser.add_argument('question',
        type=str,
        required=True,
        help="This field is required and cannot be left blank."
    )
    parser.add_argument('answer',
        type=str,
        required=True,
        help="This field is required and cannot be left blank."
    )
    parser.add_argument('intro',
        type=str,
        required=True,
        help="This field is required and cannot be left blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message":"A user with that name already exists"}, 400

        user = UserModel(data['username'], data['password'], data['question'], data['answer'], data['intro'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):
    
    def get(self, username):
        target_user = UserModel.find_by_username(username)
        if target_user:
            return {"user": target_user.json()}
        else:
            return {"message": "That username does not exist"}


