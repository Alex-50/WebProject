from requests import post

print(post("http://alex-raz-project.herokuapp.com/api/users",
           json={"id": 7, "name": "Jake", "surname": "Smith", "age": 24, "email": "jake1@mail.ru",
                 "hashed_password": "1357", "favourite": '1 2'}).json())  # корректный запрос
print(post("http://alex-raz-project.herokuapp.com/api/users",
           json={"id": 5, "surname": "Smith", "age": 24, "email": "jake@mail.ru",
                 "hashed_password": "1357"}).json())  # неполный запрос
print(post("http://alex-raz-project.herokuapp.com/api/users",
           json={"id": 1, "name": "Jake", "surname": "Smith", "age": 24, "email": "jake@mail.ru",
                 "hashed_password": "1357"}).json())  # существующий id
print(post("http://alex-raz-project.herokuapp.com/api/users",
           json={"id": 5, "name": "Jake", "surname": "Smith", "age": 24, "email": "alex@mail.ru",
                 "hashed_password": "1357"}).json())  # существующая почта
print(post("http://alex-raz-project.herokuapp.com/api/users").json())  # пустой словарь

# Вывод
"""{'success': 'OK'}
    {'error': 'Bad request'}
    {'error': 'Id or email already exists'}
    {'error': 'Id or email already exists'}
    {'error': 'Empty request'}"""
