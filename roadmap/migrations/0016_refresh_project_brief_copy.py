from copy import deepcopy

from django.db import migrations


def refresh_project_brief_copy(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model('roadmap', 'UserGoal')
    SkillNode = apps.get_model('roadmap', 'SkillNode')
    database = schema_editor.connection.alias
    active_domains = {'data_analytics', 'ai_ml', 'web_dev', 'robotics'}

    for goal in UserGoal.objects.using(database).all().iterator():
        domain = detect_domain(goal.domain, goal.goal)
        curriculum = RESTRUCTURED_CURRICULA.get(domain)
        if not curriculum:
            continue
        by_level = {item['coach_level']: item for item in curriculum['levels']}
        for node in SkillNode.objects.using(database).filter(goal_id=goal.pk, coach_level__isnull=False):
            content = by_level.get(node.coach_level)
            if content is None:
                continue
            brief = deepcopy(content['project_json'])
            if domain not in active_domains:
                brief['is_active'] = False
                brief['review_reason'] = 'Project brief is inactive.'
            node.project_json = brief
            node.save(using=database, update_fields=['project_json'])


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0015_robotics_electronics_concepts')]
    operations = [migrations.RunPython(refresh_project_brief_copy, migrations.RunPython.noop)]
