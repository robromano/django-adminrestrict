"""
adminrestrict middleware
"""

__author__ = "Robert Romano"
__copyright__ = "Copyright 2020 Robert C. Romano"


import django
import logging
import re
import socket
import sys
import ipaddress


if django.VERSION[:2] >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

from django.conf import settings
from django.http import HttpResponseForbidden

# MiddlewareMixin is only available (and useful) in Django 1.10 and
# newer versions
try:
    from django.utils.deprecation import MiddlewareMixin
    parent_class = MiddlewareMixin
except ImportError as e:
    parent_class = object


from adminrestrict.models import AllowedIP


def is_valid_ip(ip_address):
    """
    Check Validity of an IP address
    """
    valid = False
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            socket.inet_pton(family, ip_address.strip())
            valid = True
            break
        except:
            continue
    return valid


def get_ip_address_for_fqdn(fqdn):
    try:
        return socket.gethostbyname(fqdn)
    except:
        return None


def valid_fqdn(dn):
    if dn.endswith('.'):
        dn = dn[:-1]
    if len(dn) < 1 or len(dn) > 253:
        return False
    ldh_re = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$",
                        re.IGNORECASE)
    return all(ldh_re.match(x) for x in dn.split('.'))


def is_private_rfc_1918_ip(ip: str):
    """Returns true if IP is determined to be a private RFC1918 address."""
    private_ip_prefixes = getattr(settings, 'ADMINRESTRICT_PRIVATE_IP_PREFIXES',
                                  ('10.', '172.', '192.', '127.'))
    return ip.startswith(private_ip_prefixes)


def get_ip_address_from_request(request):
    """
    Makes the best attempt to get the client's real IP or return the loopback
    """
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not is_private_rfc_1918_ip(x_forwarded_for) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if is_private_rfc_1918_ip(ip):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not is_private_rfc_1918_ip(x_real_ip) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not is_private_rfc_1918_ip(remote_addr) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
            if is_private_rfc_1918_ip(remote_addr) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
        ip_address = '127.0.0.1'
    return ip_address


class AdminPagesRestrictMiddleware(parent_class):
    """
    A middleware that restricts login attempts to admin pages to
    restricted IP addresses only. Everyone else gets 403.
    """

    _invalidate_cache = True

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.disallow_get = getattr(settings, 'ADMINRESTRICT_BLOCK_GET',
                                    False)
        self.denied_msg = getattr(settings, 'ADMINRESTRICT_DENIED_MSG',
                                  "Access to admin is denied.")
        self.allow_private_ip = getattr(settings, 'ADMINRESTRICT_ALLOW_PRIVATE_IP',
                                        False)

        self.cache = {}
        self.allow_always = True
        self.logger = logging.getLogger(__name__)
        self.ipaddress_module_loaded = 'ipaddress' in sys.modules

    def request_ip_is_allowed(self, request):
        """ Returns True if the request IP is allowed based on records in
        the AllowedIP table, False otherwise."""

        if self.allow_always:
            return True

        request_ip = get_ip_address_from_request(request)

        # If the settings to allow RFC1918 private IPs is set,
        # check if request ip is a private IP and allow if so
        if self.ipaddress_module_loaded and self.allow_private_ip:
            try:
                ip = ipaddress.ip_address(request_ip)
                if ip.is_private:
                    return True
            except ValueError as e:
                logging.error(e)

        # If the request_ip is in the AllowedIP the access
        # is granted
        if self.caching_enabled() and self.cache.get(request_ip, False):
            return True
        elif AllowedIP.objects.filter(ip_address=request_ip).count() == 1:
            return True

        # Check CIDR ranges if any first
        if self.ipaddress_module_loaded:
            for cidr_range in AllowedIP.objects.filter(ip_address__regex=r"\/\d+$"):
                try:
                    net = ipaddress.ip_network(cidr_range.ip_address)
                    ip = ipaddress.ip_address(str(request_ip))
                    if ip in net:
                        return True
                except ValueError as e:
                    logging.error(e)

        # We check regular expressions defining ranges
        # of IPs. If any range contains the request_ip
        # the access is granted
        for regex_ip_range in AllowedIP.objects.filter(ip_address__endswith="*"):
            if re.match(regex_ip_range.ip_address.replace("*", ".*"), request_ip):
                return True

        for domain in AllowedIP.objects.filter(ip_address__regex=r"^[a-zA-Z]"):
            if valid_fqdn(domain.ip_address) and \
                    request_ip == get_ip_address_for_fqdn(domain.ip_address):
                return True

        # Otherwise access is not granted
        return False

    def caching_enabled(self):
        return getattr(settings, 'ADMINRESTRICT_ENABLE_CACHE',
                       False)

    def update_allow_always(self):
        # AllowedIP table empty means access is always granted
        # AllowedIP table has one entry with just '*' means access is always granted
        self.allow_always = AllowedIP.objects.count() == 0 or \
            AllowedIP.objects.filter(ip_address="*").count() == 1

    def refresh_cache(self):
        if self.caching_enabled() and AdminPagesRestrictMiddleware._invalidate_cache:
            self.cache = {}
            for ip in AllowedIP.objects.all():
                self.cache[ip] = True
            self.update_allow_always()
            AdminPagesRestrictMiddleware._invalidate_cache = False
        elif self.allow_always:
            self.update_allow_always()

    def process_request(self, request):
        """
        Check if the request is made form an allowed IP
        """
        self.refresh_cache()

        # Section adjusted to restrict login to ?edit
        # (sing cms-toolbar-login)into DjangoCMS login.
        restricted_request_uri = request.path.startswith(
            reverse(
                'admin:index') or "cms-toolbar-login" in request.build_absolute_uri()
        )

        if restricted_request_uri and request.method == 'GET':
            if self.request_ip_is_allowed(request):
                return None

            if self.disallow_get:
                return HttpResponseForbidden(self.denied_msg)
            else:
                return None

        if restricted_request_uri and request.method == 'POST':
            if not self.request_ip_is_allowed(request):
                return HttpResponseForbidden(self.denied_msg)
            else:
                return None
