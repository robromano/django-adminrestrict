try:
    __version__ = __import__('pkg_resources').get_distribution(
        'django-adminrestrict'
    ).version
except:
    __version__ = '2.0.2'


def get_version():
    return __version__
