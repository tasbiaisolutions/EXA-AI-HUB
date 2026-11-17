import json

from django.db import migrations


def refresh_curriculum_intro(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model("roadmap", "UserGoal")
    database = schema_editor.connection.alias

    for goal in UserGoal.objects.using(database).all().iterator():
        domain_key = detect_domain(goal.domain, goal.goal)
        if domain_key == "custom" and (goal.domain or "").lower().replace("/", "").replace(" ", "") in {
            "aiml",
            "ai",
        }:
            domain_key = "ai_ml"
        curriculum = RESTRUCTURED_CURRICULA.get(domain_key)
        if curriculum is None:
            continue

        try:
            metadata = json.loads(goal.roadmap_metadata or "{}")
        except (TypeError, ValueError):
            metadata = {}
        metadata.update({
            "expert_agent_name": curriculum["expert_name"],
            "expert_agent_intro": curriculum["intro"],
            "skill_nodes": curriculum["levels"],
        })
        goal.expert_agent_name = curriculum["expert_name"]
        goal.expert_agent_intro = curriculum["intro"]
        goal.roadmap_metadata = json.dumps(metadata)
        goal.save(
            using=database,
            update_fields=(
                "expert_agent_name",
                "expert_agent_intro",
                "roadmap_metadata",
            ),
        )


class Migration(migrations.Migration):
    dependencies = [
        ("roadmap", "0009_refresh_level_concepts"),
    ]

    operations = [
        migrations.RunPython(refresh_curriculum_intro, migrations.RunPython.noop),
    ]
