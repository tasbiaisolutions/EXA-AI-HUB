"""Refresh Build Lab metadata without changing lessons, quizzes, or progression data."""

from copy import deepcopy

from django.db import migrations


def refresh_build_lab_briefs(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model("roadmap", "UserGoal")
    SkillNode = apps.get_model("roadmap", "SkillNode")
    database = schema_editor.connection.alias
    active_domains = {"data_analytics", "ai_ml", "web_dev", "robotics"}

    for goal in UserGoal.objects.using(database).all().iterator():
        domain_key = detect_domain(goal.domain, goal.goal)
        curriculum = RESTRUCTURED_CURRICULA.get(domain_key)
        if curriculum is None:
            continue
        nodes = {
            node.coach_level: node
            for node in SkillNode.objects.using(database).filter(goal_id=goal.pk)
            if node.coach_level is not None
        }
        for level in curriculum["levels"]:
            node = nodes.get(level["coach_level"])
            if node is None:
                continue
            brief = deepcopy(level["project_json"])
            if domain_key not in active_domains:
                brief["is_active"] = False
                brief["review_reason"] = "Project brief is inactive."
            node.project_json = brief
            node.save(using=database, update_fields=["project_json"])


class Migration(migrations.Migration):
    dependencies = [("roadmap", "0011_usergoal_chosen_tier")]

    operations = [migrations.RunPython(refresh_build_lab_briefs, migrations.RunPython.noop)]
