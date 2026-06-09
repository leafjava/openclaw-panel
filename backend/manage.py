#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# 使用 PyMySQL 替代 mysqlclient（兼容 Django 5.2+）
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
MySQLdb.__version__ = "2.2.1"
MySQLdb.version_info = (2, 2, 1, "final", 0)


def load_env_file():
    """Load simple KEY=VALUE lines from config/.env without extra dependencies."""
    env_path = Path(__file__).resolve().parent / 'config' / '.env'
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def main():
    """Run administrative tasks."""
    load_env_file()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
