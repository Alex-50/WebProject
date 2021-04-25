from requests import delete

print(delete("http://alex-raz-project.herokuapp.com/api/users/1").json())  # корректный запрос
print(delete("http://alex-raz-project.herokuapp.com/api/users/10").json())  # несуществующий id
print(delete("http://alex-raz-project.herokuapp.com/api/users/s").json())  # некорректный id

# Вывод
"""{'success': 'OK'}
    {'error': 'Not found'}
    {'error': 'Not found'}"""
