from requests import get, post, delete

from requests import get, post, delete

# Корректный запрос
print(delete('http://localhost:5000/api/v2/user/2').json())
# Нет такого id
print(delete('http://localhost:5000/api/v2/user/20').json())
# Корректный запрос
print(post('http://localhost:5000/api/jobs',
           json={'id': 4,
                 'name': 'vasya',
                 'surname': 1,
                 'age': 15}).json())
# Нет id
print(post('http://localhost:5000/api/v2/user/',
           json={'name': 'vasya',
                 'surname': 1,
                 'age': 15}).json())
# Корректный запрос
print(get('http://localhost:5000/api/v2/user/2').json())
# Нет такого id
print(get('http://localhost:5000/api/v2/user/1').json())
