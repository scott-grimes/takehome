let exec = [
  db.createCollection('users'),
  db.createCollection('posts'),
  db.createCollection('likes')
]

printjson(exec)
