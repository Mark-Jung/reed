from flask_restful import Resource, reqparse
from flask import request
from securities.security import auth_by_token
from controllers.saved import SavedController
from models.post import PostModel
from models.user import UserModel

from werkzeug.security import safe_str_cmp

class SavedUpdate(Resource):
    """
    deals with updating the saved of user and post models.
    endpoint: /saved
    """
    parser = reqparse.RequestParser()
    parser.add_argument("mode",
            type=str,
            required=True,
            help="This field is required and cannot be left blank"
            )
    parser.add_argument("postid",
            type=str,
            required=True,
            help="This field is required and cannot be left blank"
            )
    
    def put(self):
        #two modes: append or delete
        #append:
        #1. increment that post's saved count by one
        #2. add that post id to the caller user model's saved column 
        #delete:
        #1. decrement that post's saved count by one
        #2. delete that post id to the caller user model's saved column
        auth_header = request.headers.get('Authorization')
        if auth_header:
            access_token = auth_header.split(" ")[1]
        else:
            return {"message": "This method requires an authorization header."}, 400
        error, client_id = auth_by_token(access_token)
        if error:
            return {"message": error}, 401

        data = SavedUpdate.parser.parse_args()
        mode = data['mode']
        postid = data['postid']

        if safe_str_cmp(mode, 'append'):
            # add to user's saved list
            message = SavedController.append_saved(postid, client_id)
            if message:
                return {"message": message}, 500
            # increment post's saved count
            message = SavedController.increment_post_saved(postid)
            if message:
                return {"message": message}, 500
        elif safe_str_cmp(mode, 'delete'):
            # delete post from user's saved list
            message = SavedController.delete_saved(postid, client_id)
            if message:
                return {"message": message}, 500
            # decrement posts's saved count
            message = SavedController.decrement_post_saved(postid)
            if message:
                return {"message": message}, 500
        else:
            return {"message": "Bad mode. Only append and delete available for this endpoint."}, 400
        return {"message": "Success!"}, 200

