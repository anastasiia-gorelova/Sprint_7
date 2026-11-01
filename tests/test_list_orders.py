import allure
import requests

from urls import ORDERS_URL, TIMEOUT


@allure.feature('Список заказов')
class TestListOrders:
    @allure.title('Список заказов возвращается в поле orders')
    def test_response_contains_orders_list(self):
        response = requests.get(
            ORDERS_URL, params={'limit': 10, 'page': 0}, timeout=TIMEOUT
        )
        assert response.status_code == 200, response.text
        body = response.json()
        assert 'orders' in body, body
        assert isinstance(body['orders'], list), body
        for order in body['orders']:
            assert isinstance(order, dict), order
