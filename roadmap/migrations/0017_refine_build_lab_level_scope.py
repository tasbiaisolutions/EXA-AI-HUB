from copy import deepcopy

from django.db import migrations


def refresh_level_scoped_briefs(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model('roadmap', 'UserGoal')
    SkillNode = apps.get_model('roadmap', 'SkillNode')
    database = schema_editor.connection.alias
    active_domains = {'data_analytics', 'ai_ml', 'web_dev', 'robotics'}

    for goal in UserGoal.objects.using(database).all().iterator():
        domain = detect_domain(goal.domain, goal.goal)
        curriculum = RESTRUCTURED_CURRICULA.get(domain)
        if curriculum is None:
            continue
        projects_by_level = {
            item['coach_level']: item['project_json']
            for item in curriculum['levels']
        }
        nodes = SkillNode.objects.using(database).filter(
            goal_id=goal.pk,
            coach_level__isnull=False,
        )
        for node in nodes:
            source = projects_by_level.get(node.coach_level)
            if source is None:
                continue
            brief = deepcopy(source)
            if domain not in active_domains:
                brief['is_active'] = False
                brief['review_reason'] = 'Project brief is inactive.'
            node.project_json = brief
            node.save(using=database, update_fields=['project_json'])


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0016_refresh_project_brief_copy')]
    operations = [migrations.RunPython(refresh_level_scoped_briefs, migrations.RunPython.noop)]
