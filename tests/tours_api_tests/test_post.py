from requests import post

print(post("http://127.0.0.1:5000/api/tours",
           json={"id": 5, "name": "Экскурсия по Санкт-Петербургу",
                 "places": "Дворцовая площадь&Адмиралтейство&Площадь Восстания&Московский вокзал", "cost": 3000,
                 "user": 3,
                 "date": "2021-05-21"}).json())  # корректный запрос
print(post("http://127.0.0.1:5000/api/tours",
           json={"id": 5, "name": "Экскурсия по Санкт-Петербургу", "user": 3,
                 "date": "2021-05-21"}).json())  # неполный запрос
print(post("http://127.0.0.1:5000/api/tours",
           json={"id": 2, "name": "Экскурсия по Санкт-Петербургу",
                 "places": "Дворцовая площадь&Адмиралтейство&Площадь Восстания&Московский вокзал", "cost": 3000,
                 "user": 3,
                 "date": "2021-05-21"}).json())  # существующий id
print(post("http://127.0.0.1:5000/api/tours").json())  # пустой словарь

# Вывод
"""{'success': 'OK'}
    {'error': 'Bad request'}
    {'error': 'Id already exists'}
    {'error': 'Empty request'}"""
