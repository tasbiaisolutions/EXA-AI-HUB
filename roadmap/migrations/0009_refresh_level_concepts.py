from django.db import migrations


def refresh_level_concepts(apps, schema_editor):
    from roadmap.ai_service import detect_domain
    from roadmap.course_content import RESTRUCTURED_CURRICULA

    UserGoal = apps.get_model("roadmap", "UserGoal")
    SkillNode = apps.get_model("roadmap", "SkillNode")
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

        nodes = {
            node.coach_level: node
            for node in SkillNode.objects.using(database).filter(goal_id=goal.pk)
            if node.coach_level is not None
        }
        for level in curriculum["levels"]:
            coach_level = level["coach_level"]
            node = nodes.get(coach_level)
            if node is None:
                node = SkillNode.objects.using(database).create(
                    goal_id=goal.pk,
                    name=level["name"],
                    description=level["description"],
                    importance=level["importance"],
                    order=coach_level,
                    tier=level["tier"],
                    coach_level=coach_level,
                    project_json=level["project_json"],
                )

            concepts = [
                {
                    "name": concept,
                    "description": f"Learn and practice {concept.lower()} as part of {level['name']}.",
                    "estimated_time": "15 min",
                }
                for concept in level["concepts"]
            ]
            metadata = dict(node.project_json or {})
            previous_content = {
                "name": node.name,
                "description": node.description,
                "skill_map_json": node.skill_map_json or [],
            }
            if (
                (previous_content["name"] != level["name"]
                 or previous_content["description"] != level["description"])
                and previous_content not in metadata.get("previous_course_content", [])
            ):
                metadata.setdefault("previous_course_content", []).append(previous_content)
            updated_metadata = dict(level["project_json"])
            updated_metadata["is_active"] = metadata.get(
                "is_active",
                level["project_json"]["is_active"],
            )
            updated_metadata["review_reason"] = (
                metadata.get("review_reason", "")
                if not updated_metadata["is_active"]
                else ""
            )
            updated_metadata.update({
                key: value
                for key, value in metadata.items()
                if key.startswith("previous_")
            })

            node.name = level["name"]
            node.description = level["description"]
            node.importance = level["importance"]
            node.tier = level["tier"]
            node.coach_level = coach_level
            node.skill_map_json = concepts
            node.project_json = updated_metadata
            node.save(
                using=database,
                update_fields=(
                    "name",
                    "description",
                    "importance",
                    "tier",
                    "coach_level",
                    "skill_map_json",
                    "project_json",
                ),
            )


class Migration(migrations.Migration):
    dependencies = [
        ("roadmap", "0008_restructure_course_content"),
    ]

    operations = [
        migrations.RunPython(refresh_level_concepts, migrations.RunPython.noop),
    ]
