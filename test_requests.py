from requests import post, get

jwt_token = post('http://127.0.0.1:27016/api/login', json={"login": "admin@comp.ru",
                                                "password": "qwerty"}).json()
print(jwt_token)
user = get('http://127.0.0.1:27016/api/objects', headers={'Authorization': f'Bearer {jwt_token}'})
print(user.json())

print(get('http://127.0.0.1:27016/api/history/535').json())