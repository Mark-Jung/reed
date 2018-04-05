from flask import request
from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from securities.security import auth_by_token
from werkzeug.security import safe_str_cmp

from controllers.theme import ThemeController
from controllers.user import UserController

class ThemeAdmin(Resource):
    """
    /themeadmin
    post: creates new theme
    put: edits theme
    """
    parser = reqparse.RequestParser()
    parser.add_argument("theme",
            type=str,
            required=True,
            help="This field is required."
            )
    parser.add_argument("theme_inspire",
            type=str,
            required=True,
            help="This field is required."
            )
    parser.add_argument("theme_author",
            type=str,
            required=True,
            help="This field is required."
            )
    parser.add_argument("release_time",
            type=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S'),
            required=True
            )

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return {"message": "This method requires an authorization header."}, 400
        error, client_id = auth_by_token(access_token)
        if error:
            return {"message": error}, 401
        if UserController.not_admin(client_id):
            return {"message": "Only the priveleged can come here. Get out peasant."}, 401

        data = ThemeAdmin.parser.parse_args()
        error_message = ThemeController.create_theme(data["release_time"], data["theme"], data["theme_inspire"], data["theme_author"]) 
        if error_message:
            return {"message": error_message}, 400
        else:
            return {"message": "Success!"}, 201

    def put(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return {"message": "This method requires an authorization header."}, 400
        error, client_id = auth_by_token(access_token)
        if error:
            return {"message": error}, 401
        if UserController.not_admin(client_id):
            return {"message": "Only the priveleged can come here. Get out peasant."}, 401

        data = ThemeAdmin.parser.parse_args()
        error_message = ThemeController.update_theme(data["release_time"], data["theme"], data["theme_inspire"], data["theme_author"])
        if error_message:
            return {"message": error_message}, 400
        else:
            return {"message": "Success!"}, 200

class ThemeAdminGet(Resource):

    def get(self, year, month, day):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return {"message": "This method requires an authorization header."}, 400
        error, client_id = auth_by_token(access_token)
        if error:
            return {"message": error}, 401

        if UserController.not_admin(client_id):
            return {"message": "Only the priveleged can come here. Get out peasant."}, 401
        
        if safe_str_cmp(day, "all"):
            error_message, response = ThemeController.get_for_month(year, month)
        elif day.isdigit():
            error_message, response = ThemeController.get_for_day(year, month, int(day))
        else:
            return {"message": "Unsupported mode of get"}, 400

        if error_message:
            return {"message": error_message}, 500
        else:
            return {"response": list(map(lambda x: x.json() if x else "", response))}

class Theme(Resource):

    def get(self, mode, days):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return {"message": "This method requires an authorization header."}, 400
        error, client_id = auth_by_token(access_token)
        if error:
            return {"message": error}, 401
        if safe_str_cmp(mode, "now"):
            error_message, response = ThemeController.get_now()
        elif safe_str_cmp(mode, "browse"):
            error_message, response = ThemeController.browse(int(days))
        else:
            return {"message": "Unsupported mode."}, 400

        if error_message:
            return {"message": error_message}, 500

        return {"response": list(map(lambda x: x.json() if x else None, response))}

