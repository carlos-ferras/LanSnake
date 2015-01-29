#!/usr/bin/env python
<<<<<<< HEAD
<<<<<<< HEAD
import os
import sys

if __name__ == "__main__":
=======
=======
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
"""
from django.core.management import execute_manager
import imp
try:
    imp.find_module('settings') # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n" % __file__)
    sys.exit(1)

import settings

if __name__ == "__main__":
    execute_manager(settings)
"""
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
=======
>>>>>>> 25d23941864b8ee5fbef79e4f83b8629e1d22c59
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)