"""
adminrestrict middleware
"""

__author__ = "Robert Romano (rromano@gmail.com)"
__copyright__ = "Copyright 2014 Robert C. Romano"


import django
import re
import socket

if django.VERSION[:2] >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

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
    valid = True
    try:
        socket.inet_aton(ip_address.strip())
    except:
        valid = False
    return valid


def get_ip_address_from_request(request):
    """
    Makes the best attempt to get the client's real IP or return the loopback
    """
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')
    ip_address = ''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for and ',' not in x_forwarded_for:
        if not x_forwarded_for.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_forwarded_for):
            ip_address = x_forwarded_for.strip()
    else:
        ips = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ips:
            if ip.startswith(PRIVATE_IPS_PREFIX):
                continue
            elif not is_valid_ip(ip):
                continue
            else:
                ip_address = ip
                break
    if not ip_address:
        x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
        if x_real_ip:
            if not x_real_ip.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(x_real_ip):
                ip_address = x_real_ip.strip()
    if not ip_address:
        remote_addr = request.META.get('REMOTE_ADDR', '')
        if remote_addr:
            if not remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
            if remote_addr.startswith(PRIVATE_IPS_PREFIX) and is_valid_ip(remote_addr):
                ip_address = remote_addr.strip()
    if not ip_address:
            ip_address = '127.0.0.1'
    return ip_address


class AdminPagesRestrictMiddleware(parent_class):
    """
    A middleware that restricts login attempts to admin pages to
    restricted IP addresses only. Everyone else gets 403.
    """

    def process_request(self, request):
        """
        Check if the request is made form an allowed IP
        """
        # Section adjusted to restrict login to ?edit
        # (sing cms-toolbar-login)into DjangoCMS login.
        restricted_request_uri = request.path.startswith(
            reverse('admin:index') or "cms-toolbar-login" in request.build_absolute_uri()
        )
        if restricted_request_uri and request.method == 'POST':

            # AllowedIP table emty means access is always granted
            if AllowedIP.objects.count() > 0:

                # If there are wildcard IPs access is always granted
                if AllowedIP.objects.filter(ip_address="*").count() == 0:

                    request_ip = get_ip_address_from_request(request)

                    # If the request_ip is in the AllowedIP the access
                    # is granted
                    if AllowedIP.objects.filter(ip_address=request_ip).count() == 0:

                        # We check regular expressions defining ranges
                        # of IPs. If any range contains the request_ip
                        # the access is granted
                        for regex_ip_range in AllowedIP.objects.filter(ip_address__endswith="*"):
                            if re.match(regex_ip_range.ip_address.replace("*", ".*"), request_ip):
                                return None
                        return HttpResponseForbidden("Access to admin is denied.")
