from requests import get, post, delete

print(post('http://localhost:5000/api/user',
           json={'age': 19, 'email': 'scott_chief@mars.org',
                 'id': 1, 'name': 'Scott', 'surname': 'Ridley', 'city': 'Saint-Petersburg'}).json())

