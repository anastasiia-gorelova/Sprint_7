import allure
import pytest
import requests

from urls import ORDERS_URL, TIMEOUT


@allure.feature('Создание заказа')
class TestCreateOrder:
    @allure.title('Заказ с вариантом цвета: {color}')
    @pytest.mark.parametrize(
        'color',
        [['BLACK'], ['GREY'], ['BLACK', 'GREY'], [], None],
        ids=['black', 'grey', 'both', 'empty-list', 'color-omitted'],
    )
    def test_create_order_returns_track(self, new_order, order_tracks, color):
        # None означает, что ключ color вообще не передаётся в запросе.
        if color is not None:
            new_order['color'] = color
        response = requests.post(ORDERS_URL, json=new_order, timeout=TIMEOUT)
        body = response.json()
        if 'track' in body:
            order_tracks.append(body['track'])

        assert response.status_code == 201, response.text
        assert 'track' in body, body
        assert type(body['track']) is int
        assert body['track'] > 0
