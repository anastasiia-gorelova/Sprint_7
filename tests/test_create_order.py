import allure
import pytest
import requests

from urls import ORDERS_URL, TIMEOUT


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Заказ с вариантом цвета: {color_data}')
    @pytest.mark.parametrize(
        'color_data',
        [
            {'color': ['BLACK']},
            {'color': ['GREY']},
            {'color': ['BLACK', 'GREY']},
            {'color': []},
            {},
        ],
        ids=['black', 'grey', 'both', 'empty-list', 'color-omitted'],
    )
    def test_create_order_returns_track(self, new_order, order_tracks, color_data):
        # Пустой словарь оставляет запрос без поля color.
        new_order.update(color_data)
        response = requests.post(ORDERS_URL, json=new_order, timeout=TIMEOUT)
        body = response.json()
        # get вернёт None, если track отсутствует; очистка пропустит это значение.
        order_tracks.append(body.get('track'))

        assert response.status_code == 201, response.text
        assert 'track' in body, body
        assert type(body['track']) is int
        assert body['track'] > 0
