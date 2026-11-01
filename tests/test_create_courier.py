import allure
import pytest
import requests

from data import CREATE_MISSING_MESSAGE, LOGIN_TAKEN_MESSAGE
from urls import COURIER_URL, TIMEOUT


@allure.feature('Создание курьера')
class TestCreateCourier:
    @allure.title('Создание курьера: 201 и ok=true')
    def test_create_courier(self, new_courier):
        response = requests.post(COURIER_URL, json=new_courier, timeout=TIMEOUT)
        assert response.status_code == 201, response.text
        assert response.json() == {'ok': True}, response.text

    @allure.title('Курьера можно создать без firstName')
    def test_create_courier_without_first_name(self, new_courier):
        payload = new_courier.copy()
        payload.pop('firstName')
        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        assert response.status_code == 201, response.text
        assert response.json() == {'ok': True}, response.text

    @allure.title('Повторная регистрация того же курьера запрещена')
    def test_duplicate_courier(self, registered_courier):
        response = requests.post(
            COURIER_URL, json=registered_courier, timeout=TIMEOUT
        )
        assert response.status_code == 409, response.text
        assert response.json()['message'] == LOGIN_TAKEN_MESSAGE

    @allure.title('Занятый логин с другими паролем и именем запрещён')
    def test_duplicate_login(self, registered_courier):
        payload = registered_courier.copy()
        payload['password'] = 'different_password'
        payload['firstName'] = 'Другое имя'
        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        assert response.status_code == 409, response.text
        assert response.json()['message'] == LOGIN_TAKEN_MESSAGE

    @allure.title('Создание курьера без обязательного поля {field}')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_missing_required_field(self, new_courier, field):
        # Меняем копию: исходные данные нужны фикстуре для очистки.
        payload = new_courier.copy()
        payload.pop(field)
        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == CREATE_MISSING_MESSAGE

    @allure.title('Создание курьера с пустым полем {field}')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_empty_required_field(self, new_courier, field):
        payload = new_courier.copy()
        payload[field] = ''
        response = requests.post(COURIER_URL, json=payload, timeout=TIMEOUT)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == CREATE_MISSING_MESSAGE
