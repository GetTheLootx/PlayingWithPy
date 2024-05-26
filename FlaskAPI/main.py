from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

# app.config('SQLALCHEMY_DATABASE_URI' = 'sqlite:///database.db')


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name is required to add")
video_put_args.add_argument(
    "views", type=int, help="views is required to add", required=True
)
video_put_args.add_argument(
    "likes", type=int, help="Likes is required to add", required=True
)

videos = {}


def if_not_video(video_id):
    if not video_id in videos:
        abort(404, message="video doesn't exist")


def if_is_video(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with this ID")


class Video(Resource):
    def get(self, video_id):
        if_not_video(video_id)
        return videos[video_id]

    def put(self, video_id):
        if_is_video(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    def delte(self, video_id):
        if_not_video(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5080)
