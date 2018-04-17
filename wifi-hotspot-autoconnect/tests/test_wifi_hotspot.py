import unittest
import wifi_hotspot_autoconnect as wifi


class Test_Wifi_Hotspot(unittest.TestCase):

    def test_hotspot_exists(self):
        self.assertTrue(wifi.hotspot_exists())

    def test_hotspot_autoconnect_value(self):
        self.assertIn(wifi.autoconnect_status(), {True, False})
