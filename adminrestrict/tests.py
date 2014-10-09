"""
adminrestrict tests
"""

__author__ = "Robert Romano (rromano@gmail.com)"
__copyright__ = "Copyright 2014 Robert C. Romano"

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from adminrestrict.models import AllowedIP


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo", password="bar")
        
    def test_blocked_ip(self):
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"})
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(resp.content.startswith("Access to admin is denied"))

    def test_allowed_ip(self):
        a = AllowedIP.objects.create(ip_address="127.0.0.1")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"})
        self.assertEqual(resp.status_code, 200)
        a.delete()

    def test_allow_all(self):
        a = AllowedIP.objects.create(ip_address="*")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"})
        self.assertEqual(resp.status_code, 200)
        a.delete()


        
        
