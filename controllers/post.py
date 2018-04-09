from models.post import PostModel
from models.theme import ThemeModel
from models.user import UserModel

from werkzeug.security import safe_str_cmp

class PostController():

    def create_post(theme, anonymity, writer_id, content):
        # check if that theme exists
        # check if that username exists
        # check if content is less than characters
        writer = UserModel.find_by_id(writer_id)
        if not ThemeModel.find_by_theme(theme):
            return "The post's theme doesn't exist.", None
        if not writer:
            return "The writer is not a user", None
        if len(content) > 150:
            return "The content is too long", None

        try:
            new_post = PostModel(theme, anonymity, writer_id, content)
            new_post.save_to_db()
        except:
            return "Error saving to db", None

        return ""


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

    def filter_by_writer_id(_id):
        if not _id:
            return "ID of the writer is needed", None
        if not UserModel.find_by_id(_id):
            return "A user with that id does not exist", None

        return "", PostModel.filter_by_writer_id(int(_id))

    def filter_by_theme(theme):
        """
        checks if input is valid by alphabet or number, and not blank
        returns all the post models for that theme
        """
        if not theme:
            return "Theme is needed", None
        theme_nospace = theme.replace(" ", "")
        if not theme_nospace.isalnum():
            return "Theme should only be consisted of alphabets, numbers, and spaces", None
        if not ThemeModel.find_by_theme(theme):
            return "Theme doesn't exist.", None
        try:
            return "", PostModel.filter_by_theme(theme)
        except:
            return "Error in getting most saved", None

    def filter_by_most_saved(theme):
        """
        checks if input is valid by alphabet or number, and not blank
        """
        if not theme:
            return "Theme is needed", None
        theme_nospace = theme.replace(" ", "")
        if not theme_nospace.isalnum():
            return "Theme should only be consisted of alphabets, numbers, and spaces", None
        return "", PostModel.filter_by_most_saved(theme)
