from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.post import PostModel

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
    parser.add_argument('username',
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

        new_post = PostModel(data['theme'], data['anonymity'], data['username'], data['content'])

        try:
            new_post.save_to_db()
        except:
            return {"message":"An error occured while inserting the item"}, 500

        return {"message":"Success!"}, 201


class PostList(Resource):
    def get(self, mode, key):
        if mode == 'theme':
            response = PostModel.filter_by_theme(key)
        elif mode == 'user':
            response = PostModel.filter_by_name(key)

        return {'response': list(map(lambda x: x.json(), response))}

    @jwt_required()
    def delete(self, key):
        wanted_post = find_by_id(key)
        if current_identity.username == wanted_post.username:
            wanted_post.delete_from_db
        else:
            return {'message': 'Only the writer of the post can delete the post'}
        return {'message': 'Post has been successfully deleted'}
            


