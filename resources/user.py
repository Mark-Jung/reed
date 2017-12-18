from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from controllers.user import UserController

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

    parser = reqparse.RequestParser()
    parser.add_argument('mode',
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
        )
    parser.add_argument('payload',
            type=str,
            required=False,
            help="This field is the optional payload for the request."
        )
   
    @jwt_required()
    def get(self, _id):
        target_user = UserModel.find_by_id(_id)
        if target_user:
            return {"user": target_user.json()}
        else:
            return {"message": "A user with that username does not exist"}, 400

    @jwt_required()
    def put(self, _id):
        data = User.parser.parse_args()
        caller_id = current_identity.id
        error_message, myfault = UserController.user_update(caller_id, _id, data["mode"], data["payload"])
        if error_message and myfault:
            return {"message": error_message}, 500
        elif error_message and not myfault:
            return {"message": error_message}, 400
        elif not error_message and not myfault:
            return {"message": "Success!"}, 200
        

