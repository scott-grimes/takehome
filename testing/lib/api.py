import requests

HOST_IP='server'
HOST_PORT='3000'
BASE_URL=f'http://{HOST_IP}:{HOST_PORT}'

def recent(num):
    return requests.get(f'{BASE_URL}/recent/{num}')

def post(user,password,message):
    return requests.post(f'{BASE_URL}/post',
        json = {'message':message},
        headers={'Authorization': f'{user}:{password}'})

def get_post(id):
    return requests.get(f'{BASE_URL}/get_post/{id}')

def like_post(user,password,id):
    return requests.post(f'{BASE_URL}/like/{id}',
    headers={'Authorization': f'{user}:{password}'})

def unlike_post(user,password,id):
    return requests.post(f'{BASE_URL}/unlike/{id}',
    headers={'Authorization': f'{user}:{password}'})

def delete_post(user,password,id):
    return requests.post(f'{BASE_URL}/delete_post/{id}',
    headers={'Authorization': f'{user}:{password}'})
