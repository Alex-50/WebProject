from requests import put

print(put("http://alex-raz-project.herokuapp.com/api/users/1",
          json={"age": 21, "hashed_password": "1537"}).json())  # корректный запрос
print(put("http://alex-raz-project.herokuapp.com/api/users/5",
          json={"id": 2, "age": 21, "hashed_password": "1537"}).json())  # существующий id
print(put("http://alex-raz-project.herokuapp.com/api/users/5",
          json={"email": "alex@mail.ru", "age": 21, "hashed_password": "1537"}).json())  # существующая почта

# Вывод
"""{'success': 'OK'}
    {'error': 'Id or email already exists'}
    {'error': 'Id or email already exists'}"""
