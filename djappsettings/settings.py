#!/usr/bin/env python
# vim: et ts=4 sw=4


import logging
import sys
import traceback
import importlib

from django.conf import settings as project_settings
from django.conf import global_settings


logger = logging.getLogger(__name__)


class DjAppSettings(object):
    def __init__(self):
        self._modules = None
        try:
            self._strict = project_settings.DJAPPSETTINGS_STRICT
        except:
            self._strict = True

    def _import(self, module_name, package=None):
        try:
            return importlib.import_module(
                module_name, package)

        except ImportError:

            # Python 2 tracebacks look different thant Python 3 ones.
            # If there are more than 2 tracebacks with code (traceback[3]),
            # then the ImportError was caused within an existing settings.py
            # that we were trying to import. Raise that error.
            # If there are less than 2 tracebacks with code (traceback[3]),
            # then the ImportError was caused by a missing settings.py file
            # in a module we were checking, which is OK. Don't raise that error.
            tb = sys.exc_info()[2]
            traceback_lines = [t for t in traceback.extract_tb(tb) if t[3]]
            if len(traceback_lines) > 2:
                raise

            # the exception was raised from this scope. *module_name*
            # couldn't be imported, which is fine, since allowing that
            # is the purpose of this method.
            return None

    def _setup(self):
        self._modules = []

        for module_name in project_settings.INSTALLED_APPS:
            settings_module_name = "%s.settings" % module_name
            module = self._import(settings_module_name)
            if module is None:
                continue

            # check that the app settings module doesn't contain any of
            # the settings already defined by django in global_settings.
            # Log this potentially ambiguous condition as an ERROR
            for setting_name in dir(module):
                if setting_name != setting_name.upper():
                    continue

                if hasattr(global_settings, setting_name):
                    error_message = "The '%s' module masks the built-in '%s' setting." % (
                        settings_module_name, setting_name)

                    if self._strict:
                        raise AttributeError(error_message)
                    else:
                        logger.warning(error_message)

            # check that none of the settings have already been defined
            # by another app. rather than behave ambiguously (depending
            # on which app was listed first in INSTALLED_APPS), <strike>explode</strike>...
            # Log this potentially ambiguous condition as an ERROR
            for setting_name in dir(module):
                if setting_name != setting_name.upper():
                    continue

                # ignore settings which are defined in the project's
                # settings module, to give project authors a workaround
                # for bad apps which don't PREFIX_ their settings.
                if hasattr(project_settings, setting_name):
                    continue

                for other_module in self._modules:
                    if hasattr(other_module, setting_name):
                        error_message = "The '%s' setting is already defined by the '%s' module." % (
                            setting_name, other_module)

                        if self._strict:
                            raise AttributeError(error_message)
                        else:
                            logger.warning(error_message)

            # all is well
            self._modules.append(module)

    def __getattr__(self, setting_name):
        if self._modules is None:
            self._setup()

        # try the project settings first (which also checks the global
        # default settings, which apps are NOT allowed to override).
        if hasattr(project_settings, setting_name):
            return getattr(project_settings, setting_name)

        # then try the app default settings.
        for module in self._modules:
            if hasattr(module, setting_name):
                return getattr(module, setting_name)

        raise AttributeError("The '%s' setting is not defined." % setting_name)
