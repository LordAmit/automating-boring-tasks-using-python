import unittest
import wifi_hotspot_autoconnect as wifi


class Test_Wifi_Hotspot(unittest.TestCase):

    def test_hotspot_exists(self):
        self.assertTrue(wifi.hotspot_exists())

    def test_hotspot_autoconnect_value(self):
        self.assertIn(wifi.autoconnect_status(), {True, False})

    def test_hotspot_set_autoconnect_true(self):
        wifi.autoconnect_set(True)
        self.assertTrue(wifi.autoconnect_status())

    def test_hotspot_set_autoconnect_false(self):
        wifi.autoconnect_set(False)
        self.assertFalse(wifi.autoconnect_status())

    def test_hotspot_set_autoconnect_boolean(self):
        self.test_hotspot_set_autoconnect_true()
        self.test_hotspot_set_autoconnect_false()

    def test_hotspot_set_autoconnect_incorrect(self):
        self.assertRaises(TypeError, wifi.autoconnect_set, None)
