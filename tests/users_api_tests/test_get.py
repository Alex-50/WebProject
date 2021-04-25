from requests import get

print(get("http://127.0.0.1:5000/api/users").json())  # получение всех пользователей
print(get("http://127.0.0.1:5000/api/users/1").json())  # корректный запрос на получение работы по id
print(get("http://127.0.0.1:5000/api/users/21").json())  # несуществующий id
print(get("http://127.0.0.1:5000/api/users/s").json())  # некорректный id

# Вывод
"""{'users': [{'age': 24, 'created_date': '2021-04-21 07:56:09', 'email': 'alex@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$lreFkNSp$67c5aa6c9d69ba0acedef9b86b7ff1e1e84ccc03879409c69a5239f698382569', 'id': 1, 'name': 'Alex', 'surname': 'West'}, {'age': 28, 'created_date': '2021-04-21 07:58:47', 'email': 'john@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$3ZNQOSEg$ee69d9fc4ee7a5011af96dca52e6e9b07680e997e7e08a52997e51eb282327db', 'id': 2, 'name': 'John', 'surname': 'East'}, {'age': 19, 'created_date': '2021-04-21 07:58:48', 'email': 'bill@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$resK2Uz6$994fc1906fc6ea1c1e3328647b82e707857cc57c2cdb9e56885b791fd5358abd', 'id': 3, 'name': 'Bill', 'surname': 'North'}, {'age': 32, 'created_date': '2021-04-21 09:26:29', 'email': 'mike@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$92vJqBfc$ff8061adfa35c3fe044c87e441b6ed5e0ee580572815f9e2505b45e08d90f1fc', 'id': 4, 'name': 'Mike', 'surname': 'South'}, {'age': 24, 'created_date': '2021-04-22 12:23:48', 'email': 'jake@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$FtOIrPzC$435cb571ed271d6158b66f87507a37b0fab7d941e9a0350b748cd597845fb913', 'id': 5, 'name': 'Jake', 'surname': 'Smith'}]}
    {'users': {'age': 24, 'created_date': '2021-04-21 07:56:09', 'email': 'alex@mail.ru', 'hashed_password': 'pbkdf2:sha256:150000$lreFkNSp$67c5aa6c9d69ba0acedef9b86b7ff1e1e84ccc03879409c69a5239f698382569', 'id': 1, 'name': 'Alex', 'surname': 'West'}}
    {'error': 'Not found'}
    {'error': 'Not found'}"""
