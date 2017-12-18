from models.post import PostModel

from werkzeug.security import safe_str_cmp

class PostListController():
    # more complex functions that interact with the model for the resource to use

    def filter_by_id(wanted):
        if not wanted:
            return "Wanted post list is empty", None
        # check if wanted list is only comprised of numbers and spaces
        wanted_nospace = wanted.replace(" ", "")
        if not wanted_nospace.isdigit():
            return "Post ids should only consist of integers", None
        wanted_list = wanted.split(' ')
        result = []
        for each in wanted_list:
            result.append(PostModel.find_by_id(each))
        if len(wanted_list) != len(result):
            return "Inconsistent loading of posts", None
        return "", result

    def filter_by_username(username):
        if not username:
            return "Name is needed", None
        # check if name is only comprised of numbers and spaces
        username_nospace = username.replace(" ", "")
        if not username_nospace.isalnum():
            return "Username is only made of alphabets, numbers, and spaces", None
        return "", PostModel.filter_by_username(username)

    def filter_by_theme(theme):
        if not theme:
            return "theme is needed", None
        theme_nospace = theme.replace(" ", "")
        if not theme_nospace.isalnum():
            return "theme should only be consisted of alphabets, numbers, and spaces", None
        return "", PostModel.filter_by_theme(theme)

    def filter_by_most_saved():
        try:
            return "", PostModel.filter_by_most_saved()
        except:
            return "Error in getting most saved", None





            
        

