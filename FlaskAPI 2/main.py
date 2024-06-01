from os import path
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class videoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name = {self.name}, views = {self.views}, likes= {self.likes} )"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument(
    "likes", type=int, help="Likes is required to add", required=True
)
video_put_args.add_argument(
    "name", type=str, help="name is required to add", required=True
)
video_put_args.add_argument(
    "views", type=int, help="Likes is required to add", required=True
)


video_update_args = reqparse.RequestParser()
video_update_args.add_argument("likes", type=int, help="Likes is required to add")
video_update_args.add_argument("name", type=str, help="name is required to add")
video_update_args.add_argument("views", type=int, help="Likes is required to add")

resource_field = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer,
}


class Video(Resource):
    @marshal_with(resource_field)
    def get(self, video_id):
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video ID was not found.... ")
        return result

    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = videoModel.query.filter_by(id=video_id).first()

        if result:
            abort(409, message="video Id taken.. ")

        video = videoModel(
            id=video_id, name=args["name"], views=args["views"], likes=args["likes"]
        )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = videoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="video was not found")

        for arg in args:
            if args[arg] is not None:
                setattr(result, arg, args[arg])

        db.session.commit()
        return result, 500

    def delete(self, video_id):
        if_not_video(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5080)
    if not path.exists("database.db"):
        with app.app_context():
            db.create_all()
