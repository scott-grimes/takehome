from flask import Flask
from functools import wraps
from lib.decorators import *
from flask import g, request, make_response
import lib.db as db

app = Flask(__name__)

@app.route('/post', methods=['POST'])
@valid_user
def post():
    try:
        d = request.json
        postId = db.createPost(g.user,d['message'])
        print(postId,flush=True)
        if not postId:
            return make_response({"message" : "Internal Server Error"}, 500)
        return make_response({"value" : postId}, 201)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/recent', defaults={'number': "10"})
@app.route('/recent/<string:number>', methods=['GET'])
def recent(number):
    try:
        posts = db.getPosts(int(number))
        return make_response({'value':posts}, 200)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/get_post/<string:post_id>', methods=['GET'])
@valid_post_id
def get_post(post_id):
    try:
        post = db.getPost(g.post_id)
        if not post:
            return make_response({'message': 'Not Found'}, 404)
        return make_response({'value': post}, 200)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/like/<string:post_id>', methods=['POST'])
@valid_user
@valid_post_id
def like(post_id):
    try:
        db.likePost(g.user,g.post_id)
        return make_response({"value" : post_id}, 200)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/unlike/<string:post_id>', methods=['POST'])
@valid_user
@valid_post_id
def unlike(post_id):
    try:
        db.unlikePost(g.user,g.post_id)
        return make_response({"value" : post_id}, 200)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/delete_post/<string:post_id>', methods=['POST'])
@valid_user
@valid_post_id
def delete_post(post_id):
    try:
        succeeded = db.deletePost(g.user,g.post_id)
        if not succeeded:
            return make_response({"message" : f"Unauthorized"}, 400)
        return make_response({"value" : post_id}, 202)
    except Exception as e:
        print(e,flush=True)
        return make_response({"message" : "Internal Server Error"}, 500)

@app.route('/health', methods=['GET'])
def health():
    return make_response({'Healthy':'as a Horse'}, 200)

if __name__ == "__main__":
    app.run(
        host=APP_CONF['HOST_IP'],
        port=APP_CONF['PORT'],
        debug= APP_CONF['DEBUG'] == 'true' )
