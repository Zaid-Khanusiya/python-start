from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["mydb"]

users_collection = db["users"]
posts_collection = db["posts"]

'''
curl -X POST http://127.0.0.1:5007/users \
-H "Content-Type: application/json" \
-d '{"name": "Nemesis", "email": "nemesis00@example.com"}'
----------------------------------------------------
curl -X POST http://127.0.0.1:5007/posts \
-H "Content-Type: application/json" \
-d '{"title": "My First Post", "content": "Hello from Mongo!"}'
'''
# For get query just visit /user OR /posts in browser localhost


class User(Resource):
    def post(self):
        data = request.get_json()
        users_collection.insert_one(data)
        return {"msg": "User added"}

    def get(self):
        users = list(users_collection.find({}, {"_id": 0}))
        return users

class Post(Resource):
    def post(self):
        data = request.get_json()
        posts_collection.insert_one(data)
        return {"msg": "Post added"}

    def get(self):
        posts = list(posts_collection.find({}, {"_id": 0}))
        return posts

api.add_resource(User, "/users")
api.add_resource(Post, "/posts")

if __name__ == "__main__":
    app.run(debug=True, port=5007)