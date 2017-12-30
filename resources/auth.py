from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from models.user import UserModel
from securities.security import login 


class AuthLogin(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument("username",
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
        )
    parser.add_argument("password",
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
        )
    
    def post(self):
        """
        if valid, returns token and message.
        if invalid, returns error message with 401
        if it doesn't have one of the required parameter, returns 400
        """
        data = AuthLogin.parser.parse_args()
        # response is in byte form, so must decode back to utf-8
        response = login(data["username"], data["password"])
        if response:
            return {"access_token": response.decode("utf-8"), "message": "Success!"}, 200
        else:
            return {"message": "Invalid credentials. Register first."}, 401

