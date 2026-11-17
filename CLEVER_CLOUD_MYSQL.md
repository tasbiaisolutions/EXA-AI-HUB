# Clever Cloud MySQL

The application requires MySQL and reads its database connection from the
environment variables injected by a linked Clever Cloud MySQL add-on:

- `MYSQL_ADDON_HOST`
- `MYSQL_ADDON_PORT`
- `MYSQL_ADDON_DB`
- `MYSQL_ADDON_USER`
- `MYSQL_ADDON_PASSWORD`

No database password belongs in the repository. Link the MySQL add-on to the
application in Clever Cloud, and its variables will be injected during build
and runtime. If ProxySQL is enabled, the app automatically uses
`CC_MYSQL_PROXYSQL_SOCKET_PATH` instead of the network host and port. Django
will stop at startup if a complete MySQL configuration is not available; there
is no SQLite fallback.

The project uses Django 5.2 LTS, which supports MySQL 8.0.11 and newer.

## Deploy a new database

Run Django's migrations after the add-on has been linked:

```powershell
python manage.py migrate
```

## Move the existing SQLite data

If the existing SQLite file contains data you need, export it before deploying
this revision (while the application still uses its prior SQLite settings),
then import it after switching to MySQL. Exclude Django's generated
content-type and permission data:

```powershell
python manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.Permission --indent 2 --output sqlite-data.json
python manage.py migrate
python manage.py loaddata sqlite-data.json
```

Keep `sqlite-data.json` private if it contains user data, and delete it after
you have confirmed the MySQL migration.
