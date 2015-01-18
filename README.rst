DjAppSettings: Per-App Settings for Django
==========================================

* I hate pasting blobs into my settings.py every time I enable an app.

* This is a Python module which provides a sane way for reusable Django apps to configure themselves.

* It's a drop-in replacement for the ``django.conf.settings`` class. You can fetch all of your project, app, and global default settings via a single ``settings`` object.

* It doesn't touch your project's settings module, and existing Django apps are free to ignore it. Your app can even fall back to the usual method if this module isn't available.

* App settings are prevented from clobbering `built-in settings`_. They can only *add* settings.

* Project settings (in ``DJANGO_SETTINGS_MODULE``) override app settings.

* Using per-app prefixes is a good idea, but not mandatory.

.. _built-in settings: http://code.djangoproject.com/browser/django/trunk/django/conf/global_settings.py


But, but
--------

* I'm aware of `Jared Forsyth`_'s `django-appsettings`_, and I think it's lovely but wrong. Project settings should not be editable in the Django admin.

* I'm also aware that this feature has been rejected numerous times on the Django trac. But pasting a bunch of junk into my ``settings.py`` each time I add an app is a pain in the ass.

* Checking for a setting (via ``settings.hasattr``), and falling back to a hard-coded default value is a terrible solution, because your defaults are duplicated and buried. They should be easily discoverable.

.. _Jared Forsyth: http://github.com/jabapyth
.. _django-appsettings: http://github.com/jabapyth/django-appsettings


Usage
=====

Where you would usually do something like::

    from django.conf import settings
    getattr(settings, "MY_SETTING", "DEFAULT")

Create a ``settings.py`` file in your app, containing::

    MY_SETTING = "DEFAULT"

and do something like::

    from djappsettings import settings
    settings.MY_SETTING

If you'd like to support this module where available, but fall back to the usual method if not, just ``try`` it::

    try: from djappsettings import settings
    except: from django.conf import settings
    settings.MY_SETTING


Installation
============

Via Pip::

    $ pip install djappsettings

Via GitHub::

    $ git clone git://github.com/adammck/djappsettings.git
    $ python djangoappsettings/setup.py install


Testing
=======

Install tox and run the tests::

    $ git clone git://github.com/adammck/djappsettings.git
    $ pip install tox
    $ cd djappsettings
    $ tox


Bugs?
=====

This was created to scratch an itch for the `RapidSMS`_ project. I hope it will be useful to you. Use it at your own risk. (But do use it, because it's *way* better.)

Patches and pull requests are very welcome.
Please file bugs on `GitHub`_.

.. _RapidSMS: http://rapidsms.org
.. _GitHub: http://github.com/adammck/djappsettings/issues


License
=======

djappsettings is free software, available under the BSD license.
