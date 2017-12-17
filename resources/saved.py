from flask_restful import Resource
from flask_jwt import current_identity, jwt_required
from controllers.saved import SavedController
from models.post import PostModel
from models.user import UserModel

from werkzeug.security import safe_str_cmp

class SavedUpdate(Resource):
    #deals with updating the saved of user and post models.

    @jwt_required()
    def put(self, mode, postid):
        #two modes: append or delete
        #append:
        #1. increment that post's saved count by one
        #2. add that post id to the caller user model's saved column 
        #delete:
        #1. decrement that post's saved count by one
        #2. delete that post id to the caller user model's saved column

        if safe_str_cmp(mode, 'append'):
            message = SavedController.append_saved(postid, current_identity.username)
            if message:
                return {"message": message}, 500
            message = SavedController.increment_post_saved(postid)
            if message:
                return {"message": message}, 500
        elif safe_str_cmp(mode, 'delete'):
            message = SavedController.delete_saved(postid, current_identity.username)
            if message:
                return {"message": message}, 500
            message = SavedController.decrement_post_saved(postid)
            if message:
                return {"message": message}, 500
        else:
            return {"message": "Bad mode. Only append and delete available for this endpoint."}, 400
        return {"message": "Success!"}

