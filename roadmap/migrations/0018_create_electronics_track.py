from copy import deepcopy

from django.db import migrations


def create_electronics_track(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model('roadmap', 'UserGoal')
    SkillNode = apps.get_model('roadmap', 'SkillNode')
    database = schema_editor.connection.alias
    levels = RESTRUCTURED_CURRICULA['electronics']['levels']

    for goal in UserGoal.objects.using(database).all().iterator():
        if detect_domain(goal.domain, goal.goal) != 'electronics':
            continue
        existing_nodes = list(
            SkillNode.objects.using(database).filter(goal_id=goal.pk).order_by('order', 'pk')
        )
        by_level = {}
        for node in existing_nodes:
            level_number = node.coach_level or node.order
            if 1 <= level_number <= len(levels) and level_number not in by_level:
                by_level[level_number] = node

        for index, level in enumerate(levels, 1):
            tier = level['tier']
            skill_map = [
                {
                    'name': concept,
                    'description': f'Learn and practice {concept.lower()} in {level["name"]}.',
                    'estimated_time': '15 min',
                }
                for concept in level['concepts']
            ]
            node = by_level.get(index)
            if node is None:
                SkillNode.objects.using(database).create(
                    goal_id=goal.pk,
                    name=level['name'],
                    description=level['description'],
                    importance=level['importance'],
                    status='not_started',
                    phase='assessment',
                    order=index,
                    tier=tier,
                    coach_level=index,
                    skill_map_json=skill_map,
                    current_concept_index=0,
                    project_json=deepcopy(level['project_json']),
                )
                continue

            node.name = level['name']
            node.description = level['description']
            node.importance = level['importance']
            node.order = index
            node.tier = tier
            node.coach_level = index
            node.skill_map_json = skill_map
            node.current_concept_index = min(node.current_concept_index, len(skill_map) - 1)
            node.project_json = deepcopy(level['project_json'])
            node.save(using=database, update_fields=[
                'name', 'description', 'importance', 'order', 'tier', 'coach_level',
                'skill_map_json', 'current_concept_index', 'project_json',
            ])


class Migration(migrations.Migration):
    dependencies = [('roadmap', '0017_refine_build_lab_level_scope')]
    operations = [migrations.RunPython(create_electronics_track, migrations.RunPython.noop)]
