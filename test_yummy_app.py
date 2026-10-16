import unittest
from unittest.mock import patch
from yummy_app import YummyApp
import gps_service


# ==============================================================
# CẤP ĐỘ 1: Bộ test cơ bản có sẵn (~35% Coverage)
# ==============================================================
class TestEasyLevel(unittest.TestCase):
    """Kiểm thử chức năng cơ bản tính tiền đơn hàng"""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# ==============================================================
# CẤP ĐỘ 2: Kiểm thử logic khuyến mãi & Đóng thế Mocking GPS
# ==============================================================
class TestMediumLevel(unittest.TestCase):
    """Kiểm thử chức năng apply_promo_code"""

    def test_apply_promo_online_valid(self):
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "GIAM10")
        self.assertEqual(result, 90000.0)

    def test_apply_promo_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline", os_version=15)
        with self.assertRaises(ConnectionError):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_promo_special_code_os15_success(self):
        app = YummyApp(network_status="online", os_version=15)
        result = app.apply_promo_code(100000, "NEW_OS_ONLY")
        self.assertEqual(result, 80000.0)

    def test_apply_promo_special_code_os14_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=14)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "NEW_OS_ONLY")

    def test_apply_promo_invalid_code_raises_value_error(self):
        app = YummyApp(network_status="online", os_version=15)
        with self.assertRaises(ValueError):
            app.apply_promo_code(100000, "INVALID_CODE")


class TestHardLevel(unittest.TestCase):
    """Kiểm thử đóng thế phần cứng GPS (Mocking) cho get_nearby_restaurants"""

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_in_range(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(restaurants, ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_out_of_range(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        app = YummyApp()
        restaurants = app.get_nearby_restaurants()
        self.assertEqual(restaurants, [])

    @patch('yummy_app.gps_service.get_current_location')
    def test_get_nearby_restaurants_gps_signal_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError()
        app = YummyApp()
        result = app.get_nearby_restaurants()
        self.assertEqual(result, "Khong the xac dinh vi tri.")


if __name__ == '__main__':
    unittest.main()