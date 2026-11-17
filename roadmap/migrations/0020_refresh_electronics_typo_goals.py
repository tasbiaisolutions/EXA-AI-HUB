from importlib import import_module

from django.db import migrations


def refresh_electronics_aliases(apps, schema_editor):
    UserGoal = apps.get_model('roadmap', 'UserGoal')
    database = schema_editor.connection.alias
    aliases = {'electrocics', 'electrocics engineering', 'eee'}
    for goal in UserGoal.objects.using(database).all().iterator():
        if (goal.domain or '').strip().casefold() in aliases:
            goal.domain = 'Electronics'
            goal.save(using=database, update_fields=['domain'])

    # Reapply the existing Electronics curriculum to matching goals so old generic
    # focus lists are replaced with the correct level and topic names.
    migration_0018 = import_module('roadmap.migrations.0018_create_electronics_track')
    migration_0018.create_electronics_track(apps, schema_editor)


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0019_systemadminlog_chatmessage')]
    operations = [migrations.RunPython(refresh_electronics_aliases, migrations.RunPython.noop)]
