import requests

LOGIN_URL = 'http://127.0.0.1:8000/api/auth/login/'
FAVORITE_URL = 'http://127.0.0.1:8000/api/interactions/favorites/'

login_resp = requests.post(LOGIN_URL, json={'username': 'referee', 'password': 'referee'})
print('login', login_resp.status_code, login_resp.text)
if login_resp.status_code != 200:
    raise SystemExit('login failed')
access_token = login_resp.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}
fav_resp = requests.post(FAVORITE_URL, json={'target_type': 'event', 'target_id': 1}, headers=headers)
print('favorite', fav_resp.status_code, fav_resp.text)
