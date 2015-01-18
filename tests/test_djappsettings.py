from mock import patch
import unittest

import django
from django.conf import settings as project_settings

from djappsettings import settings


class DjAppSettingsTest(unittest.TestCase):

    def setUp(self):
        if django.VERSION > (1, 7):
            django.setup()
        settings._modules = None
        settings._strict = True
        project_settings.INSTALLED_APPS = ['djappsettings']

    def test_finds_project_setting(self):
        self.assertEqual(settings.SECRET_KEY, 'not-secret')

    def test_skips_apps_without_settings(self):
        project_settings.INSTALLED_APPS = ['django.contrib.admin']
        self.assertEqual(settings.SECRET_KEY, 'not-secret')

    # patch settings._import to return a module with settings that we specify

    @patch.object(settings, '_import')
    def test_masks_global_settings_raises_error(self, mock_module):
        # Should raise AttributeError if we mask a global setting like ADMINS
        mock_module.return_value.ADMINS = 'blah'
        with self.assertRaises(AttributeError):
            settings.ADMINS

    @patch.object(settings, '_import')
    def test_masks_global_settings_not_strict(self, mock_module):
        # if DJAPPSETTINGS_STRICT is False, then don't raise error
        mock_module.return_value.ADMINS = 'blah'
        settings._strict = False
        self.assertEqual(settings.ADMINS, ())

    @patch.object(settings, '_import')
    def test_finds_module_setting(self, mock_module):
        mock_module.return_value.MODULE_SPECIFIC_SETTING = 'blah'
        self.assertEqual(settings.MODULE_SPECIFIC_SETTING, 'blah')

    @patch.object(settings, '_import')
    def test_duplicate_module_setting_raises_error(self, mock_module):
        mock_module.return_value.MODULE_SPECIFIC_SETTING = 'blah'
        # putting 2 apps in INSTALLED_APPS will make Mock try to give each of them
        # the same setting (MODULE_SPECIFIC_SETTING)
        project_settings.INSTALLED_APPS = ['django.contrib.admin', 'djappsettings']
        with self.assertRaises(AttributeError):
            settings.MODULE_SPECIFIC_SETTING
        # But hasattr should never fail
        settings._modules = None
        self.assertFalse(hasattr(settings, 'MODULE_SPECIFIC_SETTING'))

    @patch.object(settings, '_import')
    def test_duplicate_module_setting_not_strict(self, mock_module):
        mock_module.return_value.MODULE_SPECIFIC_SETTING = 'blah'
        # putting 2 apps in INSTALLED_APPS will make Mock try to give each of them
        # the same setting (MODULE_SPECIFIC_SETTING)
        project_settings.INSTALLED_APPS = ['django.contrib.admin', 'djappsettings']
        settings._strict = False
        # if DJAPPSETTINGS_STRICT is False, then don't raise error
        self.assertEqual(settings.MODULE_SPECIFIC_SETTING, 'blah')

    def test_hasattr_should_not_fail(self):
        # hasattr should return False if setting is not defined
        # Currently, it blows up with ValueError on Python 3
        self.assertFalse(hasattr(settings, 'FAKE_SETTING'))

    def test_error_in_settings_isnt_masked(self):
        project_settings.INSTALLED_APPS = ['app_with_import_error', ]
        with self.assertRaises(ImportError):
            settings.SECRET_KEY
