from datetime import date, timedelta
from uuid import uuid4


CREATE_MISSING_MESSAGE = 'Недостаточно данных для создания учетной записи'
LOGIN_TAKEN_MESSAGE = 'Этот логин уже используется. Попробуйте другой.'
LOGIN_MISSING_MESSAGE = 'Недостаточно данных для входа'
NOT_FOUND_MESSAGE = 'Учетная запись не найдена'


def courier_payload():
    # UUID делает логин уникальным при каждом запуске теста.
    return {
        'login': 'sprint7_' + uuid4().hex,
        'password': uuid4().hex,
        'firstName': 'Тестовый',
    }


def order_payload():
    return {
        'firstName': 'Тест',
        'lastName': 'Автотест',
        'address': 'Тестовая улица, дом 1',
        'metroStation': '4',
        'phone': '+79990000000',
        'rentTime': 2,
        'deliveryDate': (date.today() + timedelta(days=2)).isoformat(),
        'comment': 'Учебный тест Sprint_7',
    }
