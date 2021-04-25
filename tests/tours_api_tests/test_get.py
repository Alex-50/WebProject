from requests import get

print(get("http://alex-raz-project.herokuapp.com/api/tours").json())  # получение всех экскурсий
print(get("http://alex-raz-project.herokuapp.com/api/tours/2").json())  # корректный запрос на получение работы по id
print(get("http://alex-raz-project.herokuapp.com/api/tours/21").json())  # несуществующий id
print(get("http://alex-raz-project.herokuapp.com/api/tours/s").json())  # некорректный id

# Вывод
"""{'tours': [{'about': 'Незабываемая экскурсия по Хрустальному кольцу России!', 'cost': 20000, 'date': '2021-04-21', 'id': 1, 'name': 'Хрустальное кольцо России', 'places': 'Владимир&Гусь-хрустальный&Муром', 'user': 2}, {'about': 'Обзорная экскурсия по городу Москва', 'cost': 8000, 'date': '2021-04-25', 'id': 2, 'name': 'Обзорная экскурсия по Москве', 'places': 'Москва Красная Площадь&\nМосква Проспект Мира 1&\nМосква Курский вокзал', 'user': 1}, {'about': 'Класс', 'cost': 5000, 'date': '2021-06-12', 'id': 4, 'name': 'Экскурсия', 'places': 'Москва&\nВладимир&\nСаратов&\nЧебоксары', 'user': 4}]}
    {'tours': {'about': 'Обзорная экскурсия по городу Москва', 'cost': 8000, 'date': '2021-04-25', 'id': 2, 'name': 'Обзорная экскурсия по Москве', 'places': 'Москва Красная Площадь&\nМосква Проспект Мира 1&\nМосква Курский вокзал', 'user': 1}}
    {'error': 'Not found'}
    {'error': 'Not found'}"""
