import bcrypt
from lib.config import APP_CONF
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://%s:%s@%s:%s/'%
    (APP_CONF['DB_USER'],
    APP_CONF['DB_PASS'],
    APP_CONF['DB_HOST'],
    APP_CONF['DB_PORT'])
    )

db = client[APP_CONF['DB_NAME']]

def userExists(user):
    return db["users"].find_one({'name': user}) is not None

def upcertUser(user,password):
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    obj =  db["users"].insert_one({'name':user,'password':hashed})
    return str(obj.inserted_id)

def login(user,password):
    '''
    If user is valid return username, otherwise return None
    '''
    if not userExists(user):
        upcertUser(user,password)
        return user

    hashed = db["users"].find_one({'name': user})['password']
    return user if bcrypt.checkpw(password.encode('utf8'), hashed) else None

def createPost(user,message):
    if not db['posts'].find_one({'_id':'list'}):
        db['posts'].insert_one({'_id':'list','value':[]})
    obj = db['posts'].insert_one({'user': user, 'body': message})
    new_id = str(obj.inserted_id)
    db['posts'].update_one({'_id':'list'},{'$push': {'value': new_id}})
    return new_id

# returns up to last *num posts
def getPosts(num):
    if not db['posts'].find_one({'_id':'list'}):
        return []
    postIds = db['posts'].find_one({'_id':'list'})['value'][-num:]
    # cast objectid to strings
    arr = [db['posts'].find_one({'_id': ObjectId(id) }) for id in postIds]
    for post in arr:
        post['_id'] = str(post['_id'])
        post['likes'] = getNumLikes(post['_id'])
    return arr

def getPost(id):
    post = db['posts'].find_one({'_id':id})
    if not post:
        return None
    post['_id'] = str(post['_id'])
    return {**post, 'likes': getNumLikes(id)}

def getNumLikes(id):
    ret = db['likes'].find_one({'_id': id})
    return ret['count'] if ret is not None else 0

def deletePost(user,id):
    post = db['posts'].find_one({'_id':id})
    if not post or post['user'] != user:
        return False
    db['posts'].remove({'_id':id})
    db['likes'].remove({'_id':id})
    db['posts'].update_one({'_id':'list'},{'$pull': {'value': str(id)}})
    return True

def likePost(user,id):
    if not db['likes'].find_one({'_id': id}):
        db['likes'].insert_one({'_id': id,'users':[],'count':0})
    if user not in db['likes'].find_one({'_id': id})['users']:
        db['likes'].update_one({'_id':id},{'$push': {'users': user}, '$inc': {'count':1}})

def unlikePost(user,id):
    if db['likes'].find_one({'_id': id}) is not None:
        if user in db['likes'].find_one({'_id': id})['users']:
            db['likes'].update_one({'_id':id},{'$pull': {'users': user}, '$inc': {'count':-1}})
