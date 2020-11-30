# Django Admin Restrict

[![build-status-image]][travis]
[![coverage-status-image]][codecov]
[![pypi-version]][pypi]

**Restrict admin pages using simple IP address rules.**

## Overview

``django-adminrestrict`` secures access to the Django admin pages. It works
by blocking requests for the admin page path unless the requests come from specific IP addresses
that you specify in a model.  


## Requirements

``django-adminrestrict`` requires Django 1.4 or later.  The
application is intended improve the security around the Django admin
login pages.

## Installation

Download and install ``django-adminrestrict`` using **one** of the following methods:

### pip

You can install the latest stable package running this command:

    $ pip install django-adminrestrict

### Setuptools

You can install the latest stable package running:

    $ easy_install django-adminrestrict

## Dependencies for Python 2.7.x

`adminrestrict` has no dependencies when using Python 3.x.  Under Python 2.x, some features depend on the `ipaddress` module.  Install via `pip install ipaddress`.

## Development

You can contribute to this project forking it from github and sending pull requests.


## Configuration

First of all, you must add this project to your list of ``INSTALLED_APPS`` in
``settings.py``

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

Next, install the ``AdminPagesRestrictMiddleware`` middleware:

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'adminrestrict.middleware.AdminPagesRestrictMiddleware',
    )


Create the appropriate tables in your database that are necessary for operation.

For django(<1.7), run ``python manage.py syncdb``.

For django(>=1.7), run ``python manage.py makemigrations adminrestrict; python manage.py migrate``. 

IMPORTANT: When the package is configured in your project, an empty table called `AllowedIP`
will be created in your database. If this table is empty or has one record with
a "\*" the package will not restrict any IPs. If you want to add specific restrictions
please go to the next section.

## Usage

Using ``django-adminrestrict`` is extremely simple.  Once you install the application
and the middleware, all you need to do is update the allowed IP addresses `AllowedIP`
section of the admin pages.

### Adding allowed IP addresses

Login to the admin pages and browse to the Adminrestrict app, and
start creating recorded in the `AllowedIP` table.  Just type in the IP
addresses and save them. These will be single IPv4 addresses that are
permitted to access the pages.

### Adding allowed IP addresses with wildcards

Create a `AllowedIP` entries ending with a "\*" to any IPs that start
with the specified pattern. For example, adding `192.*` would allow
addreses starting matching 192.*.*.* to access the admin pages.

### Adding allowed IP addresses using CIDR ranges

Create a `AllowedIP` entries denoted in CIDR notation, to indicate a range 
of IP addresses that would be allowed to login/access the admin pages.
For example, a CIDR range with a suffix indicating the number of bits 
of the prefix, such as `192.0.2.0/24` for IPv4 would indicate an 
entire subnet allowed to access the admin pages.
### Adding allowed IP addresses using domain names

Create `AllowedIP` records with domain names starting with a lower-case or upper-case character. These domain names' corresponding IP addresses
will be allowed to access the admin pages. Recommended use case: dynamic 
DNS domain names.

### Adding * to disable all restrictions

Create a single `AllowedIP` record with "\*" as the IP address, to
temporarily disable restrictions. In this way, you do not have to
modify settings.py and remove the middleware if you need to disable.

Having at least one `AllowedIP` record with * as the IP address
effectively disables all restrictions.

## Advanced Settings

There are a few advanced settings that can be engaged by adding them
to your project's `settings.py` file:

`ADMINRESTRICT_BLOCK_GET=True` will block all GET requests to admin urls.  By default, `adminrestrict` only blocks the POST method to block logins only, which is usually sufficient, because GET will redirect to the login page anyway. 

`ADMINRESTRICT_ENABLE_CACHE=True` will cause `adminrestrict` to cache some of the IP addresses retrieved from the AllowedIP model to reduce read query load on your database.  When any update gets made to AllowedIP models, the cache is auto-refreshed. 

`ADMINRESTRICT_DENIED_MSG="Custom denied msg."` will let you set the response body of the 403 HTTP 
result when a request is denied. By default, the message is **"Access to admin is denied."**

`ADMINRESTRICT_ALLOW_PRIVATE_IP=True` will allow all private IP addresses to access
the admin pages, regardless of whether the request IP matches any pattern or IP address
in the AllowedIP model.  Note: private IP addresses are those which comply with [RFC1918](https://tools.ietf.org/html/rfc1918).

[build-status-image]: https://secure.travis-ci.org/robromano/django-adminrestrict.svg?branch=master
[travis]: https://travis-ci.org/robromano/django-adminrestrict?branch=master
[pypi-version]: https://badge.fury.io/py/django-adminrestrict.svg
[pypi]: https://pypi.org/project/django-adminrestrict/
[coverage-status-image]: https://img.shields.io/codecov/c/github/robromano/django-adminrestrict/master.svg
[codecov]: https://codecov.io/github/robromano/django-adminrestrict?branch=master
