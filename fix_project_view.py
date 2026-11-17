"""Fix project_view to always use stage projects from stage_projects.py"""

with open('roadmap/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Always use stage_project first, never the SkillNode's project_json
old = """    if has_active_skill_brief:
        active_brief = project_brief
        level_name = curr_skill.name
    elif stage_proj and stage_proj.get('is_active'):
        active_brief = stage_proj
        level_name = f\"{selected_stage} Project: {stage_proj['title']}\"
    else:
        return render(request, 'roadmap/project_preparing.html', {
            'goal': goal,
            'level_name': level_name,
        }, status=403)"""

new = """    # ALWAYS use the unique stage project from stage_projects.py
    # Never fall back to SkillNode's per-level project_json
    if stage_proj and stage_proj.get('is_active'):
        active_brief = stage_proj
        level_name = f\"{selected_stage} Project: {stage_proj['title']}\"
    else:
        return render(request, 'roadmap/project_preparing.html', {
            'goal': goal,
            'level_name': level_name,
        }, status=403)"""

if old in content:
    content = content.replace(old, new, 1)
    with open('roadmap/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('DONE - project_view now always uses stage project')
else:
    print('Target not found exactly, trying to find it...')
    # Check if it exists with different whitespace
    import re
    pattern = r'if has_active_skill_brief:'
    matches = [(m.start(), m.end()) for m in re.finditer(pattern, content)]
    if matches:
        print(f'Found "if has_active_skill_brief:" at positions: {matches}')
        # Show context
        for start, end in matches:
            snippet = content[max(0,start-10):start+200]
            print(f'Context: {repr(snippet[:200])}')
    else:
        print('"has_active_skill_brief" not found at all')

