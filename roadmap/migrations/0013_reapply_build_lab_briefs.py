from copy import deepcopy

from django.db import migrations


def reapply_build_lab_briefs(apps, schema_editor):
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
        for node in SkillNode.objects.using(database).filter(goal_id=goal.pk):
            level = next((item for item in curriculum["levels"] if item["coach_level"] == node.coach_level), None)
            if level is None:
                continue
            brief = deepcopy(level["project_json"])
            if domain_key not in active_domains:
                brief["is_active"] = False
                brief["review_reason"] = "Project brief is inactive."
            node.project_json = brief
            node.save(using=database, update_fields=["project_json"])


class Migration(migrations.Migration):
    dependencies = [("roadmap", "0012_refresh_build_lab_briefs")]

    operations = [migrations.RunPython(reapply_build_lab_briefs, migrations.RunPython.noop)]
