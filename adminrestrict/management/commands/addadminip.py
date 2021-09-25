from django.core.management.base import BaseCommand
from adminrestrict.models import AllowedIP


class Command(BaseCommand):
    help = 'Add a new IP address to the Admin Allowed IP table'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str)

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        ip = AllowedIP(ip_address=ip_address)
        ip.save()
        print('IP Address {0} has been added to allowed list'.format(ip_address))
