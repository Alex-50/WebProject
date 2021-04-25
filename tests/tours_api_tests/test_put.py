from requests import put

print(put("http://alex-raz-project.herokuapp.com/api/tours/1",
          json={"cost": 5000, "user": 5}).json())  # корректный запрос
print(put("http://alex-raz-project.herokuapp.com/api/tours/5",
          json={"id": 2, "name": "Экскурсия"}).json())  # существующий id

# Вывод
"""{'success': 'OK'}
    {'error': 'Id or email already exists'}"""
