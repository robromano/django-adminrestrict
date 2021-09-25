from django.core.management.base import BaseCommand
from adminrestrict.models import AllowedIP


class Command(BaseCommand):
    help = 'Remove an IP address from the Admin Allowed IP table'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str)

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        result = AllowedIP.objects.filter(ip_address=ip_address).delete()
        num = result[0]
        if num:
            print('IP Address {0} has been removed from the allowed list'.format(ip_address))
        else:
            print('IP Address {0} was not found in allowed list'.format(ip_address))
