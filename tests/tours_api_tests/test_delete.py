from requests import delete

print(delete("http://127.0.0.1:5000/api/users/4").json())  # корректный запрос
print(delete("http://127.0.0.1:5000/api/users/10").json())  # несуществующий id
print(delete("http://127.0.0.1:5000/api/users/s").json())  # некорректный id

# Вывод
"""{'success': 'OK'}
    {'error': 'Not found'}
    {'error': 'Not found'}"""
