import os
import sys
import django
from django.db import connection
from django.core.management import call_command

def fix():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Home.settings')
    django.setup()

    print("Checking for jobtech_job table...")
    with connection.cursor() as cursor:
        # Check if table exists (Postgres specific)
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'jobtech_job');")
        exists = cursor.fetchone()[0]

    if exists:
        print("Table 'jobtech_job' already exists. Proceeding with normal migrate.")
        call_command('migrate')
    else:
        print("Table 'jobtech_job' MISSING. Force-resetting JobTech migrations...")
        # 1. Clear history in django_migrations table for JobTech (fake zero)
        try:
            call_command('migrate', 'JobTech', 'zero', fake=True)
            print("Successfully faked zero for JobTech.")
        except Exception as e:
            print(f"Warning: Failed to fake zero: {e}")

        # 2. Re-apply JobTech migrations (will attempt create table)
        print("Re-applying JobTech migrations...")
        try:
            call_command('migrate', 'JobTech')
            print("Successfully re-applied JobTech migrations.")
        except Exception as e:
            print(f"Error re-applying migrations: {e}")
            # Do not exit, try global migrate anyway

        # 3. Global migrate for dependencies
        print("Running global migrate...")
        call_command('migrate')

if __name__ == '__main__':
    fix()
