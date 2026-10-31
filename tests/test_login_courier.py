import allure
import pytest
import requests

from data import LOGIN_MISSING_MESSAGE, NOT_FOUND_MESSAGE
from urls import LOGIN_URL, TIMEOUT


@allure.feature('Логин курьера')
class TestLoginCourier:
    @allure.title('Курьер авторизуется и получает свой id')
    def test_login_returns_courier_id(self, login_data):
        response = requests.post(LOGIN_URL, json=login_data, timeout=TIMEOUT)
        assert response.status_code == 200, response.text
        courier_id = response.json()['id']
        assert type(courier_id) is int
        assert courier_id > 0

        repeated_response = requests.post(
            LOGIN_URL, json=login_data, timeout=TIMEOUT
        )
        assert repeated_response.status_code == 200, repeated_response.text
        assert repeated_response.json()['id'] == courier_id

    @allure.title('Вход без обязательного поля {field}')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_missing_required_field(self, login_data, field):
        login_data.pop(field)
        response = requests.post(LOGIN_URL, json=login_data, timeout=TIMEOUT)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == LOGIN_MISSING_MESSAGE

    @allure.title('Вход с пустым полем {field}')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_empty_required_field(self, login_data, field):
        login_data[field] = ''
        response = requests.post(LOGIN_URL, json=login_data, timeout=TIMEOUT)
        assert response.status_code == 400, response.text
        assert response.json()['message'] == LOGIN_MISSING_MESSAGE

    @allure.title('Вход с неверным полем {field}')
    @pytest.mark.parametrize('field', ['login', 'password'])
    def test_wrong_credentials(self, login_data, field):
        login_data[field] += '_wrong'
        response = requests.post(LOGIN_URL, json=login_data, timeout=TIMEOUT)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == NOT_FOUND_MESSAGE

    @allure.title('Несуществующий пользователь не может войти')
    def test_nonexistent_courier(self, new_courier):
        credentials = {
            'login': new_courier['login'],
            'password': new_courier['password'],
        }
        response = requests.post(LOGIN_URL, json=credentials, timeout=TIMEOUT)
        assert response.status_code == 404, response.text
        assert response.json()['message'] == NOT_FOUND_MESSAGE
