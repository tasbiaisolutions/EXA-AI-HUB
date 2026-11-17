from django.db import migrations


TARGET_DOMAINS = {"web_dev", "data_analytics", "ai_ml", "robotics", "cybersecurity"}


def restructure_existing_courses(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model("roadmap", "UserGoal")
    SkillNode = apps.get_model("roadmap", "SkillNode")
    database = schema_editor.connection.alias

    for goal in UserGoal.objects.using(database).all().iterator():
        domain_key = detect_domain(goal.domain, goal.goal)
        normalized_domain = (goal.domain or "").lower().replace(" ", "").replace("/", "")
        if domain_key not in TARGET_DOMAINS and normalized_domain in {"aiml", "ai"}:
            domain_key = "ai_ml"
        if domain_key not in TARGET_DOMAINS:
            continue

        levels = RESTRUCTURED_CURRICULA[domain_key]["levels"]
        existing_nodes = {
            node.order: node
            for node in SkillNode.objects.using(database).filter(goal_id=goal.pk).order_by("order")
        }

        for order, level in enumerate(levels, start=1):
            node = existing_nodes.get(order)
            if node is None:
                SkillNode.objects.using(database).create(
                    goal_id=goal.pk,
                    name=level["name"],
                    description=level["description"],
                    importance=level["importance"],
                    order=order,
                    tier=level["tier"],
                    coach_level=level["coach_level"],
                    project_json=level["project_json"],
                )
                continue

            metadata = dict(node.project_json or {})
            previous_content = {
                "name": node.name,
                "description": node.description,
                "importance": node.importance,
            }
            if (
                previous_content["name"] != level["name"]
                or previous_content["description"] != level["description"]
            ):
                archived = metadata.setdefault("previous_level_content", [])
                if previous_content not in archived:
                    archived.append(previous_content)
            previous_project = {
                key: metadata[key]
                for key in ("title", "objective", "requirements", "evaluation_criteria")
                if key in metadata
            }
            if previous_project and previous_project != {
                key: level["project_json"].get(key)
                for key in previous_project
            }:
                metadata.setdefault("previous_project_briefs", []).append(previous_project)
            metadata.update(level["project_json"])

            node.name = level["name"]
            node.description = level["description"]
            node.importance = level["importance"]
            node.tier = level["tier"]
            node.coach_level = level["coach_level"]
            node.project_json = metadata
            node.save(
                using=database,
                update_fields=(
                    "name",
                    "description",
                    "importance",
                    "tier",
                    "coach_level",
                    "project_json",
                ),
            )


class Migration(migrations.Migration):
    dependencies = [
        ("roadmap", "0007_skillnode_coachlevel"),
    ]

    operations = [
        migrations.RunPython(restructure_existing_courses, migrations.RunPython.noop),
    ]
