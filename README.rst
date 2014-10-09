Django Admin Restrict
=====================

.. image:: https://secure.travis-ci.org/django-pci/django-axes.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/django-pci/django-axes

``django-adminrestrict`` enables you to block access to the Django admin pages
unless requests come from specific IP addresses.  


Requirements
============

``django-adminrestrict`` requires Django 1.4 or later.  The
application is intended improve the security around the Django admin
login pages.

Installation
============

Download and install ``django-adminrestrict`` using **one** of the following methods:

pip
---

You can install the latest stable package running this command::

    $ pip install django-adminrestrict

Setuptools
----------

You can install the latest stable package running::

    $ easy_install django-adminrestrict


Development
===========

You can contribute to this project forking it from github and sending pull requests.


Configuration
=============

First of all, you must add this project to your list of ``INSTALLED_APPS`` in
``settings.py``::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        ...
        'adminrestrict',
        ...
    )

Next, install the ``FailedLoginMiddleware`` middleware::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'adminrestrict.middleware.AdminPagesRestrictMiddleware',
    )

Run ``python manage.py syncdb``.  This creates the appropriate tables in your database
that are necessary for operation.

Usage
=====

Using ``django-adminstrict`` is extremely simple.  Once you install the application
and the middleware, all you need to do is update the allowed IP addresses `AllowedIP` 
section of the admin pages.

Adding allowed IP addresses
---------------------------

Login to the admin pages and browse to the Adminrestrict apps, and
start creating recorded in the `AllowedIP` table.  Just type in the IP
addresses and save records.

Adding wildcard to disable restrictions
---------------------------------------

Create a single `AllowedIP` record with "*" as the IP address, to
temporarily disable restrictions. In this way, you do not have to
modify settings.py and remove the middleware if you need to disable.

Having at least one `AllowedIP` record with * as the IP address 
effectively disables all restrictions.
