from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp

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

        error_message, status = UserController.create_user(data['username'], data['password'], data['question'], data['answer'], data['intro'])

        if error_message:
            return {"message": error_message}, status

        return {"message": "Success!"}, 201 

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
    def get(self, username):
        error_message, response = UserController.find_by_username(username)
        if error_message:
            return {"message": error_message} 
        else:
            return {"user": response.json()}, 400

    @jwt_required()
    def put(self, username):
        data = User.parser.parse_args()
        caller_username = current_identity.username
        error_message, myfault = UserController.user_update(caller_username, username, data["mode"], data["payload"])
        if error_message and myfault:
            return {"message": error_message}, 500
        elif error_message and not myfault:
            return {"message": error_message}, 400
        elif not error_message and not myfault:
            return {"message": "Success!"}, 200
        elif not error_message and type(myfault) is list:
            return myfault, 200

