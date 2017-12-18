from models.user import UserModel
from models.post import PostModel

from werkzeug.security import safe_str_cmp

class SavedController():

    def increment_post_saved(postid):
        target_post = PostModel.find_by_id(postid)
        if target_post is None:
            return "Target post not found"
        target_post.saved += 1
        target_post.save_to_db()
        return ""

    def decrement_post_saved(postid):
        target_post = PostModel.find_by_id(postid)
        if target_post is None:
            return "Target post not found"
        if target_post.saved > 0:
            target_post.saved -= 1
        else:
            return "Post already had saved count of 0"
        target_post.save_to_db()
        return ""
    
    def append_saved(postid, username):
        saved_list = []
        target_user = UserModel.find_by_username(username)
        #check if post id is valid
        target_post = PostModel.find_by_id(postid)
        if target_post is None:
            return "Post with the given id doesn't exist"
        #check that saved is not empty and no same posts are being added
        if target_user.saved:
            saved_list = target_user.saved.split(' ')
            for each in saved_list:
                if postid == each:
                    return "cannot add same posts multiple times"
        #check that saved count is within limit
        if target_user.saved_count > 29:
            return "Reached maximum capacity for saving posts"

        saved_list.append(postid)
        target_user.saved_count  = len(saved_list)
        target_user.saved = ' '.join(saved_list)
        target_user.save_to_db()
        return ""

    def delete_saved(postid, username):
        target_user = UserModel.find_by_username(username)
        #check if post id is valid
        target_post = PostModel.find_by_id(postid)
        if target_post is None:
            return "Post with the given id doesn't exist"
        #check that saved is not empty
        if target_user.saved:
            saved_list = target_user.saved.split(' ')
            #ensure postid exists inside user's saved list
            for each in saved_list:
                if postid == each:
                    saved_list.remove(postid)
                    target_user.saved_count = len(saved_list)
                    target_user.saved = ' '.join(saved_list)
                    target_user.save_to_db()
                    return ""
            return "target post not found for this user's saved list"
        else:
            return "saved list for this user is already empty"

