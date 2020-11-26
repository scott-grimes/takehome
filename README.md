# takehome

Fakebook is a simple communication tool backed by mongodb.

# Encryption Configuration
`.sops.yaml` shows that we using the mozilla public test key for all encryption in this repo

Import it by running
```
pushd
TMP_GIT=$(mktemp -d)
git clone https://github.com/mozilla/sops.git ${TMP_GIT}
cd ${TMP_GIT}
gpg --import pgp/sops_functional_tests_key.asc
popd
rm -rf ${TMP_GIT}
```

Then the example values.yaml file can be encrypted/decrypted as follows

```
# decrypt
sops -d -i values.yaml

# encrypt
sops -e -i --encrypted-suffix secretEnv values.yaml
```

docker volume remove takehome_mongodb_fakebook


# Local Development

Flask hot-reloading set by default `DEBUG=true` in our docker-compose file. Get started by simply...

```
# Up
docker-compose up -d
# Down
docker-compose down
```

Data is persisted using a docker volume. To start fresh remove it by running

```
docker volume remove takehome_mongodb_fakebook
```
# Test Deploy

View a test helm deploy by running the following
```
sops -d values.yaml | helm install -f - --debug --dry-run helm --generate-name
```

# Unit Tests
Unit tests can be run via docker at any time
```
docker-compose exec test python3 /srv/testing/test.py
```

# Try it Out
Image-board syle authentication is used. The first time you post you must include an auth header with your user/pass. The password for your user cannot be changed once you create it, so choose wisely!

```
# Create a Post - returns the posts id
curl -X POST localhost:3000/post -H "Authorization: myname:mypassword" -H "Content-Type: application/json" --data '{"message":"hi"}'

# See Recent Posts
curl localhost:3000/recent

# Like the most recent post!
# NOTE: Requires jq
RECENT_ID=$(curl -s localhost:3000/recent/1 | jq -r '.value[0]._id')


curl localhost:3000/get_post/${RECENT_ID}
echo "Notice the number of likes above"

curl -X POST localhost:3000/like/${RECENT_ID} -H "Authorization: myname:mypassword"

curl localhost:3000/get_post/${RECENT_ID}
echo "The likes have incremented"
```

# Helm
The `env` and `secretEnv` can be used to pass the required parameters to the deploy, the secretEnv values will be stored in a kubernetes secret - make sure your RBAC config is tight!


# Things to do
* Properly comment functions
* Better error handling
* More tests for edge cases (invalid/negative numbers, etc)
* Allow users to update passwords
* Build out cicd to deploy
* Actual flask server instead of calling python3
* Redis caching, prevent users from spamming
* ...
