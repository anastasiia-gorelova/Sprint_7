import pytest
import requests

from data import courier_payload, order_payload
from urls import CANCEL_ORDER_URL, COURIER_URL, LOGIN_URL, TIMEOUT


@pytest.fixture
def new_courier():
    data = courier_payload()
    yield data
    # Код после yield выполняется после теста, даже если проверка упала.
    credentials = {'login': data['login'], 'password': data['password']}
    response = requests.post(LOGIN_URL, json=credentials, timeout=TIMEOUT)
    if response.status_code == 404:
        # В негативных тестах курьер не должен создаваться.
        return
    response.raise_for_status()
    courier_id = response.json()['id']
    response = requests.delete(f'{COURIER_URL}/{courier_id}', timeout=TIMEOUT)
    response.raise_for_status()


@pytest.fixture
def registered_courier(new_courier):
    response = requests.post(COURIER_URL, json=new_courier, timeout=TIMEOUT)
    response.raise_for_status()
    return new_courier


@pytest.fixture
def login_data(registered_courier):
    return {
        'login': registered_courier['login'],
        'password': registered_courier['password'],
    }


@pytest.fixture
def new_order():
    return order_payload()


@pytest.fixture
def order_tracks():
    # Тест добавляет сюда track, чтобы фикстура могла отменить заказ.
    tracks = []
    yield tracks
    for track in tracks:
        # Если API не вернул track, отменять нечего; тест проверит его наличие.
        if track is not None:
            response = requests.put(
                CANCEL_ORDER_URL, params={'track': track}, timeout=TIMEOUT
            )
            response.raise_for_status()
