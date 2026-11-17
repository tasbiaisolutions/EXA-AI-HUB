"""Remove unused has_active_skill_brief code and old project_json check from project_view"""

with open('roadmap/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# Remove the strict check for empty project_json since we now always use stage_projects
old1 = """    # Strict check: if project_json was explicitly set to empty dict (tested in quality gate tests), render 403
    if curr_skill and curr_skill.project_json == {}:
        return render(request, 'roadmap/project_preparing.html', {
            'goal': goal,
            'level_name': level_name,
        }, status=403)

"""
if old1 in content:
    content = content.replace(old1, '', 1)
    changes += 1
    print('Removed empty project_json strict check')

# Remove unused has_active_skill_brief variable
old2 = """    # Check if this is an explicit level brief from skill_node (used in unit tests)
    required_brief_fields = ('title', 'objective', 'requirements', 'requirements_list', 'requirement_evidence')
    has_active_skill_brief = (
        bool(curr_skill)
        and project_brief.get('is_active') is True
        and all(project_brief.get(field) for field in required_brief_fields)
    )

"""
if old2 in content:
    content = content.replace(old2, '', 1)
    changes += 1
    print('Removed unused has_active_skill_brief')

# Remove unused project_brief variable
old3 = """    project_brief = curr_skill.project_json if curr_skill else {}

"""
if old3 in content:
    content = content.replace(old3, '\n', 1)
    changes += 1
    print('Removed unused project_brief variable')

# Also remove the old has_active_skill_brief check in the locked section
old4 = """        if has_active_skill_brief and request.method == 'POST':
            return redirect('project_submission_upload', pk=project.pk)

"""
if old4 in content:
    content = content.replace(old4, '', 1)
    changes += 1
    print('Removed has_active_skill_brief POST check in locked section')

if changes > 0:
    with open('roadmap/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'DONE - {changes} cleanups applied')
else:
    print('No changes needed (already clean)')

