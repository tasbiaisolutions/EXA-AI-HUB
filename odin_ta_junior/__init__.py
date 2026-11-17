"""Project package configuration."""

import pymysql


# Django's MySQL backend imports ``MySQLdb``. PyMySQL provides the compatible
# implementation without requiring system-level MySQL development libraries.
pymysql.install_as_MySQLdb()
