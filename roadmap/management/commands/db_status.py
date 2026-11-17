from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.utils import DatabaseError

from roadmap.models import DatabaseConnectionStatus


class Command(BaseCommand):
    help = 'Checks the cloud MySQL connection and prints its status to the terminal.'

    def handle(self, *args, **options):
        database = connection.settings_dict
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                cursor.fetchone()
        except DatabaseError as exc:
            message = f'Cloud MySQL connection failed ({type(exc).__name__}).'
            self.stderr.write(self.style.ERROR(message))
            raise CommandError(message) from exc

        database_name = str(database['NAME'])
        host = str(database.get('HOST') or 'ProxySQL socket')
        details = 'Cloud MySQL connection is active.'
        DatabaseConnectionStatus.objects.update_or_create(
            source=DatabaseConnectionStatus.SOURCE_CLOUD,
            defaults={
                'database_name': database_name,
                'host': host,
                'is_connected': True,
                'details': details,
            },
        )
        self.stdout.write(self.style.SUCCESS('=' * 72))
        self.stdout.write(self.style.SUCCESS('DATABASE CONNECTION STATUS'))
        self.stdout.write(self.style.SUCCESS('=' * 72))
        self.stdout.write(self.style.SUCCESS(f'Active DB : MySQL - {database_name}@{host}'))
        self.stdout.write(self.style.SUCCESS('Cloud MySQL connected successfully.'))
