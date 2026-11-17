import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'odin_ta_junior.settings'
django.setup()
from roadmap.stage_projects import STAGE_PROJECTS

print("=" * 100)
print(f"{'DOMAIN':<20} | {'STAGE':<15} | TITLE")
print("=" * 100)
titles = set()
for domain in STAGE_PROJECTS:
    for stage in ('Beginner', 'Intermediate', 'Advanced'):
        proj = STAGE_PROJECTS[domain].get(stage, {})
        title = proj.get('title', 'MISSING')
        dup = " ** DUPLICATE **" if title in titles else ""
        titles.add(title)
        print(f"{domain:<20} | {stage:<15} | {title}{dup}")
    print("-" * 100)

print(f"\nTotal unique projects: {len(titles)}")
print(f"Expected: 18")

