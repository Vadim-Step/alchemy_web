from requests import get, post, delete

from requests import get, post, delete

# Корректный запрос
print(delete('http://localhost:5000/api/v2/jobs/2').json())
# Нет такого id
print(delete('http://localhost:5000/api/v2/jobs/20').json())
# Корректный запрос
print(post('http://localhost:5000/api/v2/jobs',
           json={'id': 4,
                 'team_leader': 1,
                 'job': 'fix doors',
                 'work_size': 2}).json())
# Нет id
print(post('http://localhost:5000/api/v2/joobs/',
           json={'team_leader': 1,
                 'job': 'fix doors',
                 'work_size': 2}).json())
# Корректный запрос
print(get('http://localhost:5000/api/v2/jobs/2').json())
# Нет такого id
print(get('http://localhost:5000/api/v2/jobs/99').json())
