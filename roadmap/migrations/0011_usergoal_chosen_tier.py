from django.db import migrations, models


def backfill_chosen_tier(apps, schema_editor):
    UserGoal = apps.get_model('roadmap', 'UserGoal')
    database = schema_editor.connection.alias
    valid_tiers = {'Beginner', 'Intermediate', 'Advanced'}
    for goal in UserGoal.objects.using(database).all().iterator():
        goal.chosen_tier = (
            goal.current_level
            if goal.current_level in valid_tiers
            else 'Beginner'
        )
        goal.save(using=database, update_fields=['chosen_tier'])


class Migration(migrations.Migration):
    dependencies = [
        ('roadmap', '0010_refresh_curriculum_intro'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergoal',
            name='chosen_tier',
            field=models.CharField(
                choices=[
                    ('Beginner', 'Beginner'),
                    ('Intermediate', 'Intermediate'),
                    ('Advanced', 'Advanced'),
                ],
                default='Beginner',
                max_length=20,
            ),
        ),
        migrations.RunPython(backfill_chosen_tier, migrations.RunPython.noop),
    ]
