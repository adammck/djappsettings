Django App Settings
===================

* I hate pasting blobs into my settings.py every time I enable an app.

* This is a Python module which provides a sane way for reusable Django apps to configure themselves.

* It's a drop-in replacement for the `django.conf.settings` class. You can fetch all of your project, app, and global default settings via a single `settings` object.

* It doesn't touch your project's settings module, and existing Django apps are free to ignore it. Your app can even fall back to the usual method if this module isn't available.

* App settings are prevented from clobbering [built-in settings](http://code.djangoproject.com/browser/django/trunk/django/conf/global_settings.py). They can only *add* settings.

* Project settings (in DJANGO_SETTINGS_MODULE) override app settings.

* Using per-app prefixes is a good idea, but not mandatory.


But, but
--------

* I'm aware of [Jared Forsyth](http://github.com/jabapyth)'s [django-appsettings](http://github.com/jabapyth/django-appsettings), and I think it's lovely but wrong. Project settings should not be editable in the Django admin.

* I'm also aware that this feature has been rejected numerous times on the Django trac. But pasting a bunch of junk into my settings.py each time I add an app is a pain in the ass.

* I saw [this snippet](http://www.djangosnippets.org/snippets/573/). It's insufficient.

* Checking for a setting (via settings.hasattr), and falling back to a hard-coded default value is a terrible solution, because your defaults are duplicated and buried. They should be easily discoverable.


Usage
-----

Where you would usually do something like:

    from django.conf import settings
    getattr(settings, "MY_SETTING", "DEFAULT")

Create a `settings.py` file in your app, containing:

    MY_SETTING = "DEFAULT"

and do something like:

    from djangoappsettings import settings
    settings.MY_SETTING

If you'd like to support this module where available, but fall back to the usual method if not, just `try` it:

    try: from djangoappsettings import settings
    except: from django.conf import settings
    settings.MY_SETTING


Installation
------------

    $ git clone git://github.com/adammck/django-app-settings.git
    $ cd django-app-settings
    $ python setup.py install


Bugs!
-----

This was created to scratch an itch for the [RapidSMS](http://rapidsms.org) project. I hope it will be useful to others, but it doesn't have any docs or tests yet, and hasn't been field tested. There are almost certainly bugs. Use it at your own risk. (But do use it, because it's *way* better.)

Patches and pull requests are very welcome.
Please file bugs on [GitHub](http://github.com/adammck/django-app-settings/issues).
