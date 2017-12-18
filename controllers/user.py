from models.user import UserModel

from werkzeug.security import safe_str_cmp

class UserController():

    def user_update(caller_id, interactor_id, mode, payload):
        if safe_str_cmp(mode, "follow"):
            return follow(caller_id, interactor_id)
        elif safe_str_cmp(mode, "unfollow"):
            return unfollow(caller_id, interator_id)
        elif safe_str_cmp(mode, "get_following"):
            return get_following(_id)
        elif safe_str_cmp(mode, "get_followed_by"):
            return get_followed_by(_id)
        else:
            return "Unsupported mode for edit", False

    def follow(caller_id, interactor_id):
        following_list = []
        followed_by_list = []
        interactor = UserModel.find_by_id(interactor_id)
        if interactor is None:
            return "Invalid user id for interactor", False
        caller = UserModel.find_by_id(caller_id)

        if caller.following:
            following_list = caller.following.split(' ')
            for each in following_list:
                if each == interactor.id:
                    return "Cannot follow the same person twice", False
        following_list.append(interactor.id)
        caller.following_count = len(following_list)
        caller.following = ' '.join(following_list)
        try:
            caller.save_to_db()
        except:
            return "Error saving to db", True

        if interactor.followed_by:
            followed_by_list = interactor.followed_by.split(' ')
            for each in followed_by:
                if each == caller.id:
                    return "Cannot be followed by the same person twice", False
        followed_by_list.append(caller.id)
        interactor.followed_by_count = len(followed_by_list)
        interactor.followed_by = ' '.join(followed_by_list)
        try:
            interactor.save_to_db()
        except:
            return "Error saving to db", True

        return "", False

    def unfollow(caller_id, interactor_id):
        interactor = UserModel.find_by_id(interactor_id)
        if interactor is None:
            return "Invalid user id for interactor", False
        caller = UserModel.find_by_id(caller_id)
        caller_valid = False
        interactor_valid = False
        following_list = []
        followed_by_list = []

        if caller.following:
            following_list = caller.following.split(' ')
            for each in following_list:
                if interactor_id == each:
                    caller_valid = True
        if interactor.followed_by:
            followed_by_list = interactor.followed_by.split(' ')
            for each in followed_by_list:
                if caller_id == each:
                    interactor_valid = True

        if caller_valid and interactor_valid:
            following_list.remove(interactor_id)
            caller.following_count = len(following_list)
            caller.following = ' '.join(following_list)
            caller.save_to_db()
            followed_by_list.remove(caller_id)
            interactor.followed_by_count = len(followed_by_list)
            interactor.followed_by = ' '.join(followed_by_list)
            interactor.save_to_db()
            return "", False
        else:
            return "Caller or Interactor, following or followed_by is already empty or invalid", True

    def get_following(target_id):
        target_user = UserModel.find_by_id(target_id)
        if not target_user:
            return "Invalid target user id", False
        return filter_by_id(target_user.following)

    def get_followed_by(target_id):
        target_user = UserModel.find_by_id(target_id)
        if not target_user:
            return "Invalid target user id", False
        return filter_by_id(target_user.followed_by)

    def filter_by_id(wanted):
        if not wanted:
            return "Wanted user list is empty", None
        wanted_nospace = wanted.replace(" ", "")
        if not wanted_nospace.isdigit():
            return "User ids should only consist of integers", None
        wanted_list - wanted.split(' ')
        result = []
        for each in wanted_list:
            target_user = UserModel.find_by_id(each)
            if target_user is None:
                return "Invalid user id is among the list", None
            else:
                result.append(target_user.username)
        if len(wanted_list) != len(result):
            return "Inconsistent loading of users", None
        return "", result
