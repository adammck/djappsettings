import unittest
from djappsettings import settings


class DjAppSettingsTest(unittest.TestCase):

    def test_import(self):
        self.assertTrue(settings)
