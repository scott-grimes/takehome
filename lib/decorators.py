from functools import wraps
from flask import request, g
from lib.config import APP_CONF
from bson.objectid import ObjectId
from lib.db import login
#import json
from flask import make_response

def valid_user(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        try:
            headers = request.headers
            if 'Authorization' not in headers:
                return make_response({"message": "No Authorization Found"}, 401)
            auth = headers.get("Authorization")
            user, password = auth.split(':',1)
            user = login(user, password)
            if not user:
                return make_response({"message": "Invalid Authorization"}, 401)
            g.user = user
            return fun(*args, **kwargs)
        except Exception as e:
            return make_response({"message": "Interal Server Error"}, 500)
    return wrapped


def valid_post_id(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        try:
            post_id = kwargs['post_id']
            # attempt to cast
            g.post_id = ObjectId(post_id)
            return fun(*args, **kwargs)
        except Exception as e:
            return make_response({"message": f"Invalid postId: {post_id}"}, 400)
    return wrapped
