from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from controllers.post import PostController, PostListController

class Post(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('theme',
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
    )
    parser.add_argument('anonymity',
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
    )
    parser.add_argument('content',
            type=str,
            required=True,
            help="This field is required and cannot be left blank."
    )

    @jwt_required()
    def post(self):
        data = Post.parser.parse_args()

        error_message = PostController.create_post(data['theme'], data['anonymity'], current_identity.username, data['content'])
        if error_message:
            return {"message": error_message}, 400

        return {"message":"Success!"}, 201


class PostList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('wanted',
            type=str,
            required=True,
            help="List of ids of posts wanted."
    )

    def get(self, mode, key):
        error_message = ""

        if safe_str_cmp(mode, 'theme'):
            error_message, response = PostListController.filter_by_theme(key)
        elif safe_str_cmp(mode, 'user'):
            error_message, response = PostListController.filter_by_username(key)
        elif safe_str_cmp(mode, 'saved'):
            error_message, response = PostListController.filter_by_most_saved()
        else:
            error_message = "Wrong mode. Try theme, user, or saved"

        if error_message:
            return {"message": error_message}, 400

        return {"response": list(map(lambda x: x.json() if x else None, response))}

    def post(self, mode, key):
        data = PostList.parser.parse_args()
        error_message = "Wrong mode. Try id"

        if safe_str_cmp(mode, 'id') and safe_str_cmp(key, "please"):
            error_message, response = PostListController.filter_by_id(data['wanted'])

        if error_message:
            return {"message": error_message}, 400
        if response[0] is None:
            return {"message": "First id requested or the id requested is invalid"}

        return {"response": list(map(lambda x: x.json() if x else None, response))}

    @jwt_required()
    def delete(self, key):
        wanted_post = find_by_id(key)

        if current_identity.username == wanted_post.username:
            wanted_post.delete_from_db()
        else:
            return {'message': 'Only the writer of the post can delete the post'}, 400

        return {'message': 'Post has been successfully deleted'}

