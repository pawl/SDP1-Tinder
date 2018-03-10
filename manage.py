#!/usr/bin/env python
import os
import sys
from django.conf import settings


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sdp1_tinder.settings")
    # see django_boilerplate/settings/__init__.py
    os.environ.setdefault("APP_ENV", "dev")
    if settings.DEBUG:
        error_code = os.system("sass static/stylesheets/scss/myTinder.scss static/stylesheets/css/myTinder.css")
        if error_code > 0:
            print("Warning: Failed to compile SCSS files. Make sure you have LESS CSS installed.")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
