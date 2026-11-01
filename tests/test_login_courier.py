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
        body = response.json()
        courier_id = body.get('id')

        assert response.status_code == 200, response.text
        assert 'id' in body, body
        assert type(courier_id) is int
        assert courier_id > 0

    @allure.title('Повторный вход возвращает тот же id курьера')
    def test_repeated_login_returns_same_id(self, login_data):
        first_response = requests.post(LOGIN_URL, json=login_data, timeout=TIMEOUT)
        repeated_response = requests.post(
            LOGIN_URL, json=login_data, timeout=TIMEOUT
        )
        first_body = first_response.json()
        repeated_body = repeated_response.json()

        assert first_response.status_code == 200, first_response.text
        assert repeated_response.status_code == 200, repeated_response.text
        assert 'id' in first_body, first_body
        assert 'id' in repeated_body, repeated_body
        assert first_body['id'] == repeated_body['id']

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
