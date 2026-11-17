import os


def inspect_db():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odin_ta_junior.settings')

    import django

    django.setup()

    from django.db import connection

    cursor = connection.cursor()
    
    # 1. Tables check
    tables = connection.introspection.table_names()
    
    print("=" * 60)
    print("1. DATABASE TABLES & ROW COUNTS")
    print("=" * 60)
    for t in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {connection.ops.quote_name(t)}')
        count = cursor.fetchone()[0]
        print(f"  • {t:32} : {count} rows")
        
    print("\n" + "=" * 60)
    print("2. USER GOALS (Human-Readable)")
    print("=" * 60)
    from roadmap.models import SkillNode, UserGoal

    goals = UserGoal.objects.order_by('-id')[:10]
    for g in goals:
        print(f"Goal #{g.id}:")
        print(f"  User   : {g.user_name}")
        print(f"  Goal   : {g.goal}")
        print(f"  Domain : {g.domain}")
        print(f"  Level  : {g.current_level}")
        print(f"  Expert : {g.expert_agent_name}")
        print(f"  Created: {g.created_at}")
        print("-" * 40)

    print("\n" + "=" * 60)
    print("3. SAMPLE SKILL NODES")
    print("=" * 60)
    for skill in SkillNode.objects.order_by('id')[:6]:
        print(
            f"Skill #{skill.id} (Goal #{skill.goal_id}): {skill.name} "
            f"[Status: {skill.status}, Phase: {skill.phase}]"
        )
        
    connection.close()

if __name__ == '__main__':
    inspect_db()
