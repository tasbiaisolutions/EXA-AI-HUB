from django.db import migrations


def refresh_electronics_topics(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model('roadmap', 'UserGoal')
    SkillNode = apps.get_model('roadmap', 'SkillNode')
    concepts = RESTRUCTURED_CURRICULA['robotics']['levels'][0]['concepts']
    database = schema_editor.connection.alias
    for goal in UserGoal.objects.using(database).all().iterator():
        if detect_domain(goal.domain, goal.goal) != 'robotics':
            continue
        SkillNode.objects.using(database).filter(goal_id=goal.pk, coach_level=1).update(
            skill_map_json=[{'name': name, 'description': f'Learn and practice {name.lower()} as part of Level 1: Electronics basics.', 'estimated_time': '15 min'} for name in concepts]
        )


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0014_project_submission')]
    operations = [migrations.RunPython(refresh_electronics_topics, migrations.RunPython.noop)]
