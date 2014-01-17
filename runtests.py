#!/usr/bin/env python
import sys

from os.path import dirname, abspath

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3'}},
        INSTALLED_APPS=[
            'vies',
        ]
    )

from django.test.runner import DiscoverRunner


def runtests(*test_args):
    if not test_args:
        test_args = ['vies']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)
    failures = DiscoverRunner().run_tests(test_args, verbosity=1, interactive=True)
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests(*sys.argv[1:])
