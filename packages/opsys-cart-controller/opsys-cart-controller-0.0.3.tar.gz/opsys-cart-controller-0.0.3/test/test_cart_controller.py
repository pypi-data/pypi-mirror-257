import unittest
from unittest.mock import patch, MagicMock
from opsys_cart_controller.cart_controller import CartController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(CartController, 'setup_cart_motor')
    def test_setup_cart_motor(self, cart_mock: MagicMock):
        cart = CartController()
        cart.setup_cart_motor()
        cart_mock.assert_called_once_with()

    @ patch.object(CartController, 'move_to_start')
    def test_move_to_start(self, cart_mock: MagicMock):
        cart = CartController()
        cart.move_to_start()
        cart_mock.assert_called_once_with()

    @ patch.object(CartController, 'move_to_end')
    def test_move_to_end(self, cart_mock: MagicMock):
        cart = CartController()
        cart.move_to_end()
        cart_mock.assert_called_once_with()

    @ patch.object(CartController, 'move_cart_motor')
    def test_move_cart_motor(self, cart_mock: MagicMock):
        cart = CartController()
        distance = 15
        cart.move_cart_motor(dest=distance)
        cart_mock.assert_called_once_with(dest=15)

    @ patch.object(CartController, 'get_distance')
    def test_get_distance(self, cart_mock: MagicMock):
        cart = CartController()
        cart.get_distance()
        cart_mock.assert_called_once_with()

    @ patch.object(CartController, 'stop_cart')
    def test_stop_cart(self, cart_mock: MagicMock):
        cart = CartController()
        cart.stop_cart()
        cart_mock.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
