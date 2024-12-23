# Задача №1 unit-tests

# 1

import pytest


def check_age(age: int):
    if age >= 18:  # Введите условие для проверки возраста
        result = 'Доступ разрешён'
    else:
        result = 'Доступ запрещён'
    return result


@pytest.mark.parametrize("age, expected_result", [
    (17, 'Доступ запрещён'),
    (18, 'Доступ разрешён'),
    (25, 'Доступ разрешён')
])
def test_check_age(age, expected_result):
    assert check_age(age) == expected_result

# 2


def check_auth(login: str, password: str):

    if login == 'admin' and password == 'password': # Здесь напишите свой код для проверки условия
        result = 'Добро пожаловать' # В этом блоке напишите код, который выполнится, если условие True. Используйте result, как в задании выше
    else:
        result = 'Доступ ограничен' # В этом блоке напишите код, который выполнится, если условие False. Используйте result, как в задании выше

    return result


@pytest.mark.parametrize("login, password, expected_result", [
    ("admin", "password", "Добро пожаловать"),
    ("wrong_login", "password", "Доступ ограничен"),
    ("admin", "wrong_password", "Доступ ограничен")
])
def test_check_auth(login, password, expected_result):
    assert check_auth(login, password) == expected_result

# 3


def get_cost(weight: int):
    if weight <= 10:
        result = "Стоимость доставки: 200 руб."
    else:
        result = "Стоимость доставки: 500 руб."  # Напишите здесь свой код для задания, используйте конструкцию вывода как в примере выше
    return result


@pytest.mark.parametrize("weight, expected_result", [
    (5, "Стоимость доставки: 200 руб."),
    (10, "Стоимость доставки: 200 руб."),
    (11, "Стоимость доставки: 500 руб.")
])
def test_get_cost(weight, expected_result):
    assert get_cost(weight) == expected_result



