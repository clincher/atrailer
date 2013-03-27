#!/usr/bin/env python
import sys
import cbsettings


if __name__ == "__main__":
    cbsettings.configure("atrailer.settings.Settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
