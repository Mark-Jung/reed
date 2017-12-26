from models.user import UserModel

from werkzeug.security import safe_str_cmp

class UserController():

    def user_update(caller_username, interactor_username, mode, payload):
        if safe_str_cmp(mode, "follow"):
            return UserController.follow(caller_username, interactor_username)
        elif safe_str_cmp(mode, "unfollow"):
            return UserController.unfollow(caller_username, interactor_username)
        elif safe_str_cmp(mode, "get_following"):
            return UserController.get_following(interactor_username)
        elif safe_str_cmp(mode, "get_followed_by"):
            return UserController.get_followed_by(interactor_username)
        else:
            return "Unsupported mode for edit.", False

    def follow(caller_username, interactor_username):
        following_list = []
        followed_by_list = []
        interactor = UserModel.find_by_username(interactor_username)
        if interactor is None:
            return "Invalid user id for interactor.", False
        caller = UserModel.find_by_username(caller_username)
        if safe_str_cmp(caller_username, interactor_username):
            return "Can't follow self.", False
        caller_id_str = str(caller.id)
        interactor_id_str = str(interactor.id)

        if caller.following:
            following_list = caller.following.split(' ')
            for each in following_list:
                if safe_str_cmp(each, interactor_id_str):
                    return "Cannot follow the same person twice.", False
        if interactor.followed_by:
            followed_by_list = interactor.followed_by.split(' ')
            for each in followed_by_list:
                if safe_str_cmp(each, caller_id_str):
                    return "Cannot be followed by the same person twice.", False

        following_list.append(interactor_id_str)
        caller.following_count = len(following_list)
        caller.following = ' '.join(following_list)
        try:
            caller.save_to_db()
        except:
            return "Error saving to db.", True
        followed_by_list.append(caller_id_str)
        interactor.followed_by_count = len(followed_by_list)
        interactor.followed_by = ' '.join(followed_by_list)
        try:
            interactor.save_to_db()
        except:
            return "Error saving to db.", True

        return "", False

    def unfollow(caller_username, interactor_username):
        interactor = UserModel.find_by_username(interactor_username)
        if interactor is None:
            return "Invalid user id for interactor.", False
        caller = UserModel.find_by_username(caller_username)
        caller_valid = False
        interactor_valid = False
        following_list = []
        followed_by_list = []
        caller_id_str = str(caller.id)
        interactor_id_str = str(interactor.id)

        if caller.following:
            following_list = caller.following.split(' ')
            for each in following_list:
                if safe_str_cmp(each, interactor_id_str):
                    caller_valid = True
        if interactor.followed_by:
            followed_by_list = interactor.followed_by.split(' ')
            for each in followed_by_list:
                if safe_str_cmp(each, caller_id_str):
                    interactor_valid = True

        if caller_valid and interactor_valid:
            following_list.remove(interactor_id_str)
            caller.following_count = len(following_list)
            caller.following = ' '.join(following_list)
            try:
                caller.save_to_db()
            except:
                return "Error saving to db.", True
            followed_by_list.remove(caller_id_str)
            interactor.followed_by_count = len(followed_by_list)
            interactor.followed_by = ' '.join(followed_by_list)
            try:
                interactor.save_to_db()
            except:
                return "Error saving to db.", True
            return "", False
        else:
            return "Caller or Interactor, following or followed_by is already empty or invalid.", True

    def get_following(target_username):
        target_user = UserModel.find_by_username(target_username)
        if not target_user:
            return "Invalid target user id.", False
        return UserController.filter_by_id(target_user.following)

    def get_followed_by(target_username):
        target_user = UserModel.find_by_username(target_username)
        if not target_user:
            return "Invalid target user id.", False
        return UserController.filter_by_id(target_user.followed_by)

    def filter_by_id(wanted):
        if not wanted:
            return "Wanted user's list is empty.", False
        wanted_nospace = wanted.replace(" ", "")
        if not wanted_nospace.isdigit():
            return "User ids should only consist of integers.", True
        wanted_list = wanted.split(' ')
        result = []
        for each in wanted_list:
            target_user = UserModel.find_by_id(each)
            if target_user is None:
                return "Invalid user id is among the list.", True
            else:
                result.append(target_user.username)
        if len(wanted_list) != len(result):
            return "Inconsistent loading of users.", True 
        return "", result

    def not_admin(input_user):
        return not safe_str_cmp("mark", input_user.username)

    def find_by_username(username):
        target_user = UserModel.find_by_username(username)
        if target_user:
            return "", target_user
        else:
            return "A user with that username doesn't exist.", None

    def create_user(username, password, question, answer, intro):
        if UserModel.find_by_username(username):
            return "The username is already taken", 400
        if not username or not password or not question or not answer or not intro:
            return "all fields are required", 400

        try:
            new_user = UserModel(username, password, question, answer, intro)
            new_user.save_to_db()
            return "", 201
        except:
            return "Error in creating and saving user", 500

