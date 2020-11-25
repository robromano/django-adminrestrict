"""
adminrestrict tests
"""

__author__ = "Robert Romano"
__copyright__ = "Copyright 2021 Robert C. Romano"

from django.test import TestCase
from django.contrib.auth.models import User
try:
    from django.core.urlresolvers import reverse
except ImportError as e:
    from django.urls import reverse

from adminrestrict.models import AllowedIP


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="foo", password="bar")

    def test_disallow_get(self):
        a = AllowedIP.objects.create(ip_address="10.10.0.1")        
        with self.settings(ADMINRESTRICT_BLOCK_GET=True):
            resp = self.client.get("/admin/")
            self.assertEqual(resp.status_code, 403)
        a.delete()
            
    def test_allow_get_initial_page(self):
        a = AllowedIP.objects.create(ip_address="10.10.0.1")
        resp = self.client.get("/admin/")
        self.assertIn(resp.status_code, [200, 302])
        a.delete()

    def test_get_redirected(self):
        a = AllowedIP.objects.create(ip_address="10.10.0.1")
        resp = self.client.get("/admin/adminrestrict/allowedip/")
        self.assertEqual(resp.status_code, 302)
        a.delete()
        
    def test_allow_all_if_empty(self):
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"})
        self.assertIn(resp.status_code, [200, 302])

    def test_allowed_ip(self):
        a = AllowedIP.objects.create(ip_address="127.0.0.1")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        a.delete()

    def test_allowed_wildcard(self):
        a = AllowedIP.objects.create(ip_address="127.0*")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        a.delete()

    def test_blocked_no_wildcard_match(self):
        a = AllowedIP.objects.create(ip_address="16*")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
        self.assertEqual(resp.status_code, 403)
        a.delete()

    def test_default_denied_msg(self):
        DENIED_MSG = b"Access to admin is denied."
        a = AllowedIP.objects.create(ip_address="16*")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, DENIED_MSG)
        a.delete()
        
    def test_custom_denied_msg(self):
        DENIED_MSG = b"denied!"
        a = AllowedIP.objects.create(ip_address="16*")
        with self.settings(ADMINRESTRICT_DENIED_MSG=DENIED_MSG):
            resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
            self.assertEqual(resp.status_code, 403)
            self.assertEqual(resp.content, DENIED_MSG)
        a.delete()
        
    def test_allow_all(self):
        a = AllowedIP.objects.create(ip_address="*")
        resp = self.client.post("/admin/", data={'username':"foo", 'password':"bar"}, follow=True)
        self.assertEqual(resp.status_code, 200)
        a.delete()




