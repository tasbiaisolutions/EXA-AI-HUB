from django.contrib import admin
from django import forms
from .models import (
    UserGoal, SkillNode, LearningUnit, Project, Assessment, SkillAssessment,
    QuizQuestion, QuizAttempt, ConceptMasteryAttempt, ChatMessage, SystemAdminLog,
)

admin.site.register(UserGoal)


class SkillNodeAdminForm(forms.ModelForm):
    is_active = forms.BooleanField(
        required=False,
        label='Visible to learners',
        help_text='Inactive levels are hidden from learner dashboards.',
    )

    class Meta:
        model = SkillNode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        metadata = self.instance.project_json or {}
        self.fields['is_active'].initial = metadata.get('is_active', True)

    def save(self, commit=True):
        node = super().save(commit=False)
        metadata = dict(node.project_json or {})
        metadata['is_active'] = self.cleaned_data['is_active']
        if metadata['is_active']:
            metadata['review_reason'] = ''
        elif not metadata.get('review_reason'):
            metadata['review_reason'] = 'Project brief is inactive.'
        node.project_json = metadata
        if commit:
            node.save()
            self.save_m2m()
        return node


@admin.register(SkillNode)
class SkillNodeAdmin(admin.ModelAdmin):
    form = SkillNodeAdminForm
    list_display = ('name', 'goal', 'order', 'tier', 'coach_level', 'is_active')
    list_filter = ('tier', 'status')
    search_fields = ('name', 'goal__goal', 'goal__domain')
    ordering = ('goal', 'order')

    @admin.display(boolean=True, description='Active')
    def is_active(self, obj):
        return (obj.project_json or {}).get('is_active', True)


admin.site.register(LearningUnit)
admin.site.register(Project)
admin.site.register(Assessment)
admin.site.register(SkillAssessment)
admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt)
admin.site.register(ConceptMasteryAttempt)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'domain', 'level', 'panel', 'role', 'created_at')
    list_filter = ('domain', 'panel', 'role', 'created_at')
    search_fields = ('user__goal', 'user__domain', 'content')
    readonly_fields = ('created_at',)


@admin.register(SystemAdminLog)
class SystemAdminLogAdmin(admin.ModelAdmin):
    list_display = ('category', 'message', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('message',)
    readonly_fields = ('category', 'message', 'created_at')
