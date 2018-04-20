import unittest
import library.hotspot_wrapper as wifi


class Test_Wifi_Hotspot(unittest.TestCase):

    def test_hotspot_exists(self):
        self.assertTrue(wifi.hotspot_exists())

    def test_hotspot_autoconnect_value(self):
        self.assertIn(wifi.status_hotspot_autoconnect(), {True, False})

    def test_hotspot_set_autoconnect_true(self):
        wifi.set_autoconnect(True)
        self.assertTrue(wifi.status_hotspot_autoconnect())

    def test_hotspot_set_autoconnect_false(self):
        wifi.set_autoconnect(False)
        self.assertFalse(wifi.status_hotspot_autoconnect())

    def test_hotspot_set_autoconnect_boolean(self):
        self.test_hotspot_set_autoconnect_true()
        self.test_hotspot_set_autoconnect_false()

    def test_hotspot_set_autoconnect_incorrect(self):
        self.assertRaises(TypeError, wifi.set_autoconnect, None)
