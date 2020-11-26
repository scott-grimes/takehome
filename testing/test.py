import json
from lib.api import *

def ensure(title, fun, params, code, truthFunction):
    try:
        resp = fun(*params)
        assert (resp.status_code == code),title
        returned_obj = resp.json()
        assert (truthFunction(returned_obj)),title
        print(title)
    except Exception:
        print(title,': FAILED!')
        print('Response was:')
        print(resp.status_code)
        print(resp.json())
        exit(1)

for i in range(15):
    ensure(f'Can post {i}/15',post,['admin','password','my message'], 201,
        lambda x: True )

ensure('Can fetch 5 posts',recent,[5], 200,
    lambda x: len(x['value']) == 5)

ensure('Can fetch 10 posts',recent,[10], 200,
    lambda x: len(x['value']) == 10)

ensure('Cannot post with invalid auth',post,['admin','hax0rs','my message'], 401,
    lambda x: x['message'] == 'Invalid Authorization')

last_post_id = recent(1).json()['value'][0]['_id']

ensure('Can read a post', get_post,[last_post_id], 200,
    lambda x: x['value']['_id'] == last_post_id)

ensure('Can like a post', like_post,['seconduser','password1',last_post_id], 200,
    lambda x: x['value'] == last_post_id)

ensure('Count computed correctly after liking', get_post,[last_post_id], 200,
    lambda x: x['value']['likes'] == 1)

ensure('Liking Previous Post Has No Effect', like_post,['seconduser','password1',last_post_id], 200,
    lambda x: x['value'] == last_post_id)

ensure('Count computed correctly after liking twice', get_post,[last_post_id], 200,
    lambda x: x['value']['likes'] == 1)

ensure('Can dislike a post', unlike_post,['seconduser','password1',last_post_id], 200,
    lambda x: x['value'] == last_post_id)

ensure('Count computed correctly after unliking', get_post,[last_post_id], 200,
    lambda x: x['value']['likes'] == 0)

ensure('Cannot delete others post', delete_post,['seconduser','password1',last_post_id], 400,
    lambda x: x['message'] == 'Unauthorized')

ensure('Cannot delete post with invalid credentials', delete_post,['admin','password1',last_post_id], 401,
    lambda x: x['message'] == 'Invalid Authorization')

ensure('Can delete post', delete_post,['admin','password',last_post_id], 202,
    lambda x: x['value'] == last_post_id)

ensure('Cannot retrieve deleted post', get_post,[last_post_id], 404,
    lambda x: x['message'] == 'Not Found')

ensure('Cannot like invalid post', like_post,['admin','password','fakepostid'], 400,
    lambda x: x['message'] == 'Invalid postId: fakepostid')

print('All tests successful')
